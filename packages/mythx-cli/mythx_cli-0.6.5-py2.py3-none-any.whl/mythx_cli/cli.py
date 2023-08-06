"""The main runtime of the MythX CLI."""
import logging
import sys
import time
from glob import glob
from os.path import abspath, commonpath
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import click
import htmlmin
import jinja2
from mythx_models.response import (
    AnalysisInputResponse,
    AnalysisListResponse,
    AnalysisStatusResponse,
    DetectedIssuesResponse,
    GroupCreationResponse,
    GroupListResponse,
)
from pythx import Client, MythXAPIError
from pythx.middleware.group_data import GroupDataMiddleware
from pythx.middleware.toolname import ClientToolNameMiddleware

from mythx_cli import __version__
from mythx_cli.formatter import FORMAT_RESOLVER, util
from mythx_cli.formatter.base import BaseFormatter
from mythx_cli.payload import (
    generate_bytecode_payload,
    generate_solidity_payload,
    generate_truffle_payload,
)

DEFAULT_HTML_TEMPLATE = Path(__file__).parent / "templates/default.html"
DEFAULT_MD_TEMPLATE = Path(__file__).parent / "templates/default.md"
RGLOB_BLACKLIST = ["node_modules"]
LOGGER = logging.getLogger("mythx-cli")
logging.basicConfig(level=logging.WARNING)


@click.pass_obj
def write_or_print(ctx, data: str, mode="a+") -> None:
    """Depending on the context, write the given content to stdout or a given
    file.

    :param ctx: Click context holding group-level parameters
    :param data: The data to print or write to a file
    :param mode: The mode to open the file in (if file output enabled)
    :return:
    """

    if not ctx["output"]:
        click.echo(data)
        return
    with open(ctx["output"], mode) as outfile:
        outfile.write(data + "\n")


class APIErrorCatcherGroup(click.Group):
    """A custom click group to catch API-related errors.

    This custom Group implementation catches :code:`MythXAPIError`
    exceptions, which get raised when the API returns a non-200
    status code. It is used to notify the user about the error that
    happened instead of triggering an uncaught exception traceback.

    It is given to the main CLI entrypoint and propagated to all
    subcommands.
    """

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except MythXAPIError as exc:
            click.echo("The API returned an error:\n{}".format(exc))
            sys.exit(1)


# noinspection PyIncorrectDocstring
@click.group(cls=APIErrorCatcherGroup)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    envvar="MYTHX_DEBUG",
    help="Provide additional debug output",
)
@click.option(
    "--api-key", envvar="MYTHX_API_KEY", help="Your MythX API key from the dashboard"
)
@click.option(
    "--username", envvar="MYTHX_USERNAME", help="Your MythX account's username"
)
@click.option(
    "--password", envvar="MYTHX_PASSWORD", help="Your MythX account's password"
)
@click.option(
    "--format",
    "fmt",
    default="table",
    type=click.Choice(FORMAT_RESOLVER.keys()),
    show_default=True,
    help="The format to display the results in",
)
@click.option(
    "--ci",
    is_flag=True,
    default=False,
    help="Return exit code 1 if high-severity issue is found",
)
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    default=False,
    help="Do not prompt for any confirmations",
)
@click.option(
    "-o", "--output", default=None, help="Output file to write the results into"
)
@click.pass_context
def cli(ctx, **kwargs) -> None:
    """Your CLI for interacting with https://mythx.io/

    \f

    :param ctx: Click context holding group-level parameters
    :param debug: Boolean to enable the `logging` debug mode
    :param api_key: User JWT api token from the MythX dashboard
    :param username: The MythX account ETH address/username
    :param password: The account password from the MythX dashboard
    :param fmt: The formatter to use for the subcommand output
    :param ci: Boolean to return exit code 1 on medium/high-sev issues
    :param output: Output file to write the results into
    """

    ctx.obj = dict(kwargs)
    ctx.obj["retval"] = 0
    toolname_mw = ClientToolNameMiddleware(name="mythx-cli-{}".format(__version__))
    if kwargs["api_key"] is not None:
        ctx.obj["client"] = Client(api_key=kwargs["api_key"], middlewares=[toolname_mw])
    elif kwargs["username"] and kwargs["password"]:
        ctx.obj["client"] = Client(
            username=kwargs["username"],
            password=kwargs["password"],
            middlewares=[toolname_mw],
        )
    else:
        raise click.UsageError(
            (
                "The trial user has been deprecated. You can still use the MythX CLI for free "
                "by signing up for a free account at https://mythx.io/ and entering your access "
                "credentials."
            )
        )
    if kwargs["debug"]:
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).setLevel(logging.DEBUG)


@cli.group()
def group() -> None:
    """Create, modify, and view analysis groups.

    \f

    This subcommand holds all group-related actions, such as creating,
    listing, closing groups, as well as fetching the status of one
    or more group IDs.
    """
    pass


@cli.group()
def analysis() -> None:
    """Get information on running and finished analyses.

    \f

    This subcommand holds all analysis-related actions, such as submitting new
    analyses, listing existing ones, fetching their status, as well as fetching
    the reports of one or more finished analysis jobs.
    """
    pass


def sanitize_paths(job: Dict) -> Dict:
    """Remove the common prefix from paths.

    This method takes a job payload, iterates through all paths, and
    removes all their common prefixes. This is an effort to only submit
    information on a need-to-know basis to MythX. Unless it's to distinguish
    between files, the API does not need to know the absolute path of a file.
    This may even leak user information and should be removed.

    If a common prefix cannot be found (e.g. if there is just one element in
    the source list), the relative path from the current working directory
    will be returned.

    This concerns the following fields:
    - sources
    - AST absolute path
    - legacy AST absolute path
    - source list
    - main source

    :param job: The payload to sanitize
    :return: The sanitized job
    """

    source_list = job.get("source_list")
    if not source_list:
        # triggers on None and empty list
        # if no source list is given, we are analyzing bytecode only
        return job
    source_list = [abspath(s) for s in source_list]
    if len(source_list) > 1:
        # get common path prefix and remove it
        prefix = commonpath(source_list) + "/"
    else:
        # fallback: replace with CWD and get common prefix
        prefix = commonpath(source_list + [str(Path.cwd())]) + "/"

    job["source_list"] = [s.replace(prefix, "") for s in source_list]
    if job.get("main_source") is not None:
        job["main_source"] = job["main_source"].replace(prefix, "")
    for name in list(job.get("sources", {})):
        data = job["sources"].pop(name)
        # sanitize AST data in compiler output
        for ast_key in ("ast", "legacyAST"):
            if not (data.get(ast_key) and data[ast_key].get("absolutePath")):
                continue
            sanitized_absolute = data[ast_key]["absolutePath"].replace(prefix, "")
            data[ast_key]["absolutePath"] = sanitized_absolute

        # replace source key names
        job["sources"][name.replace(prefix, "")] = data

    return job


def is_valid_job(job) -> bool:
    """Detect interface contracts.

    This utility function is used to detect interface contracts in solc and Truffle
    artifacts. This is done by checking whether any bytecode or source maps are to be
    found in the speficied job. This check is performed after the payload has been
    assembled to cover Truffle and Solidity analysis jobs.

    :param job: The payload to perform the check on
    :return: True if the submitted job is for an interface, False otherwise
    """

    filter_values = ("", "0x", None)
    if all(
        (
            job.get("bytecode") in filter_values,
            job.get("source_map") in filter_values,
            job.get("deployed_source_map") in filter_values,
            job.get("deployed_bytecode") in filter_values,
        )
    ):
        click.echo(
            "Skipping submission for contract {} because no bytecode was produced.".format(
                job["contract_name"]
            )
        )
        return True
    return False


def find_truffle_artifacts(project_dir: Union[str, Path]) -> Optional[List[str]]:
    """Look for a Truffle build folder and return all relevant JSON artifacts.

    This function will skip the Migrations.json file and return all other files
    under :code:`<project-dir>/build/contracts/`. If no files were found,
    :code:`None` is returned.

    :param project_dir: The base directory of the Truffle project
    :return: Files under :code:`<project-dir>/build/contracts/` or :code:`None`
    """

    output_pattern = Path(project_dir) / "build" / "contracts" / "*.json"
    artifact_files = list(glob(str(output_pattern.absolute())))
    if not artifact_files:
        return None

    return [f for f in artifact_files if not f.endswith("Migrations.json")]


def find_solidity_files(project_dir: str) -> Optional[List[str]]:
    """Return all Solidity files in the given directory.

    This will match all files with the `.sol` extension.

    :param project_dir: The directory to search in
    :return: Solidity files in `project_dir` or `None`
    """

    output_pattern = Path(project_dir)
    artifact_files = [str(x) for x in output_pattern.rglob("*.sol")]
    if not artifact_files:
        return None

    return [af for af in artifact_files if all((b not in af for b in RGLOB_BLACKLIST))]


def walk_solidity_files(
    ctx, solc_version: str, base_path: Optional[str] = None, remappings: Tuple[str] = None
) -> List[Dict]:
    """Aggregate all Solidity files in the given base path.

    Given a base path, this function will recursively walk through the filesystem
    and aggregate all Solidity files it comes across. The resulting job list will
    contain all the Solidity payloads (optionally compiled), ready for submission.

    :param ctx: :param ctx: Click context holding group-level parameters
    :param solc_version: The solc version to use for Solidity compilation
    :param base_path: The base path to walk through from
    :param remappings: Import remappings to pass to solcx
    :return:
    """

    jobs = []
    remappings = remappings or []
    walk_path = Path(base_path) if base_path else Path.cwd()
    files = find_solidity_files(walk_path)
    consent = ctx["yes"] or click.confirm(
        "Do you really want to submit {} Solidity files?".format(len(files))
    )
    if not consent:
        sys.exit(0)
    LOGGER.debug("Found Solidity files to submit:\n{}".format("\n".join(files)))
    for file in files:
        jobs.extend(generate_solidity_payload(file, solc_version, remappings))
    return jobs


@cli.command()
@click.argument("target", default=None, nargs=-1, required=False)
@click.option(
    "--async/--wait",  # TODO: make default on full
    "async_flag",
    help="Submit the job and print the UUID, or wait for execution to finish",
)
@click.option(
    "--mode",
    type=click.Choice(["quick", "standard", "deep"]),
    default="quick",
    show_default=True,
)
@click.option(
    "--create-group",
    is_flag=True,
    default=False,
    help="Create a new group for the analysis",
)
@click.option(
    "--group-id",
    type=click.STRING,
    help="The group ID to add the analysis to",
    default=None,
)
@click.option(
    "--group-name",
    type=click.STRING,
    help="The group name to attach to the analysis",
    default=None,
)
@click.option(
    "--min-severity",
    type=click.STRING,
    help="Ignore SWC IDs below the designated level",
    default=None,
)
@click.option(
    "--swc-blacklist",
    type=click.STRING,
    help="A comma-separated list of SWC IDs to ignore",
    default=None,
)
@click.option(
    "--swc-whitelist",
    type=click.STRING,
    help="A comma-separated list of SWC IDs to include",
    default=None,
)
@click.option(
    "--solc-version",
    type=click.STRING,
    help="The solc version to use for compilation",
    default=None,
)
@click.option(
    "--include",
    type=click.STRING,
    multiple=True,
    help="The contract name(s) to submit to MythX",
    default=None,
)
@click.option(
    "--remap-import",
    type=click.STRING,
    multiple=True,
    help="Add a solc compilation import remapping",
    default=None,
)
@click.pass_obj
def analyze(
    ctx,
    target: List[str],
    async_flag: bool,
    mode: str,
    create_group: bool,
    group_id: str,
    group_name: str,
    min_severity: str,
    swc_blacklist: str,
    swc_whitelist: str,
    solc_version: str,
    include: Tuple[str],
    remap_import: Tuple[str]
) -> None:
    """Analyze the given directory or arguments with MythX.

    \f

    :param ctx: Click context holding group-level parameters
    :param target: Arguments passed to the `analyze` subcommand
    :param async_flag: Whether to execute the analysis asynchronously
    :param mode: Full or quick analysis mode
    :param create_group: Create a new group for the analysis
    :param group_id: The group ID to add the analysis to
    :param group_name: The group name to attach to the analysis
    :param min_severity: Ignore SWC IDs below the designated level
    :param swc_blacklist: A comma-separated list of SWC IDs to ignore
    :param swc_whitelist: A comma-separated list of SWC IDs to include
    :param solc_version: The solc version to use for Solidity compilation
    :param include: List of contract names to send - exclude everything else
    :param remap_import: List of import remappings to pass on to solc
    :return:
    """

    group_name = group_name or ""
    if create_group:
        resp: GroupCreationResponse = ctx["client"].create_group(group_name=group_name)
        group_id = resp.group.identifier
        group_name = resp.group.name or ""

    if group_id:
        # associate all following analyses to the passed or newly created group
        group_mw = GroupDataMiddleware(group_id=group_id, group_name=group_name)
        ctx["client"].handler.middlewares.append(group_mw)

    jobs = []
    include = list(include)

    if not target:
        if Path("truffle-config.js").exists() or Path("truffle.js").exists():
            files = find_truffle_artifacts(Path.cwd())
            if not files:
                raise click.exceptions.UsageError(
                    (
                        "Could not find any truffle artifacts. Are you in the project root? "
                        "Did you run truffle compile?"
                    )
                )
            LOGGER.debug(
                "Detected Truffle project with files:\n{}".format("\n".join(files))
            )
            for file in files:
                jobs.append(generate_truffle_payload(file))

        elif list(glob("*.sol")):
            jobs = walk_solidity_files(ctx=ctx, solc_version=solc_version, remappings=remap_import)
        else:
            raise click.exceptions.UsageError(
                "No argument given and unable to detect Truffle project or Solidity files"
            )
    else:
        for target_elem in target:
            target_split = target_elem.split(":")
            element, suffix = target_split[0], target_split[1:]
            include += suffix
            if element.startswith("0x"):
                LOGGER.debug(f"Identified target {element} as bytecode")
                jobs.append(generate_bytecode_payload(element))
            elif Path(element).is_file() and Path(element).suffix == ".sol":
                LOGGER.debug(f"Trying to interpret {element} as a solidity file")
                jobs.extend(
                    generate_solidity_payload(file=element, version=solc_version, contracts=suffix, remappings=remap_import)
                )
            elif Path(element).is_dir():
                files = find_truffle_artifacts(Path(element))
                if files:
                    # extract truffle artifacts if config found in target
                    jobs.extend([generate_truffle_payload(file) for file in files])
                else:
                    # recursively enumerate sol files if not a truffle project
                    jobs.extend(
                        walk_solidity_files(ctx, solc_version, base_path=element)
                    )
            else:
                raise click.exceptions.UsageError(
                    f"Could not interpret argument {element} as bytecode or Solidity file"
                )

    # sanitize local paths
    jobs = [sanitize_paths(job) for job in jobs]
    # filter jobs where no bytecode was produced
    jobs = [job for job in jobs if not is_valid_job(job)]
    # reduce to whitelisted contract names
    if include:
        found_contracts = {job["contract_name"] for job in jobs}
        overlap = set(include).difference(found_contracts)
        if overlap:
            raise click.UsageError(
                f"The following contracts could not be found: {', '.join(overlap)}"
            )
        jobs = [job for job in jobs if job["contract_name"] in include]

    uuids = []
    with click.progressbar(jobs) as bar:
        for job in bar:
            # attach execution mode, submit, poll
            job.update({"analysis_mode": mode})
            resp = ctx["client"].analyze(**job)
            uuids.append(resp.uuid)

    if async_flag:
        write_or_print("\n".join(uuids))
        return

    issues_list: List[
        Tuple[DetectedIssuesResponse, Optional[AnalysisInputResponse]]
    ] = []
    formatter: BaseFormatter = FORMAT_RESOLVER[ctx["fmt"]]
    for uuid in uuids:
        while not ctx["client"].analysis_ready(uuid):
            # TODO: Add poll interval option
            time.sleep(3)
        resp: DetectedIssuesResponse = ctx["client"].report(uuid)
        inp: Optional[AnalysisInputResponse] = ctx["client"].request_by_uuid(
            uuid
        ) if formatter.report_requires_input else None

        util.filter_report(
            resp,
            min_severity=min_severity,
            swc_blacklist=swc_blacklist,
            swc_whitelist=swc_whitelist,
        )
        # extend response with job UUID to keep formatter logic isolated
        resp.uuid = uuid
        issues_list.append((resp, inp))

    write_or_print(formatter.format_detected_issues(issues_list))
    sys.exit(ctx["retval"])


@analysis.command("status")
@click.argument("uuids", default=None, nargs=-1)
@click.pass_obj
def analysis_status(ctx, uuids: List[str]) -> None:
    """Get the status of an already submitted analysis.

    \f

    :param ctx: Click context holding group-level parameters
    :param uuids: A list of job UUIDs to fetch the status for
    """
    for uuid in uuids:
        resp = ctx["client"].status(uuid)
        write_or_print(FORMAT_RESOLVER[ctx["fmt"]].format_analysis_status(resp))


@group.command("list")
@click.option(
    "--number",
    default=5,
    type=click.IntRange(min=1, max=100),  # ~ 5 requests à 20 entries
    show_default=True,
    help="The number of most recent groups to display",
)
@click.pass_obj
def group_list(ctx, number: int) -> None:
    """Get a list of analysis groups.

    \f

    :param ctx: Click context holding group-level parameters
    :param number: The number of analysis groups to display
    :return:
    """

    client: Client = ctx["client"]
    result = GroupListResponse(groups=[], total=0)
    offset = 0
    while True:
        resp = client.group_list(offset=offset)
        if not resp.groups:
            break
        offset += len(resp.groups)
        result.groups.extend(resp.groups)
        if len(result.groups) >= number:
            break

    # trim result to desired result number
    LOGGER.debug(resp.total)
    result = GroupListResponse(groups=result[:number], total=resp.total)
    write_or_print(FORMAT_RESOLVER[ctx["fmt"]].format_group_list(result))


@group.command("status")
@click.argument("gids", default=None, nargs=-1)
@click.pass_obj
def group_status(ctx, gids: List[str]) -> None:
    """Get the status of an analysis group.

    \f

    :param ctx: Click context holding group-level parameters
    :param gids: A list of group IDs to fetch the status for
    """

    for gid in gids:
        resp = ctx["client"].group_status(group_id=gid)
        write_or_print(FORMAT_RESOLVER[ctx["fmt"]].format_group_status(resp))


@group.command("open")
@click.argument("name", default="", nargs=1)
@click.pass_obj
def group_open(ctx, name: str) -> None:
    """Create a new group to assign future analyses to.

    \f

    :param ctx: Click context holding group-level parameters
    :param name: The name of the group to be created (autogenerated if empty)
    """

    resp: GroupCreationResponse = ctx["client"].create_group(group_name=name)
    write_or_print(
        "Opened group with ID {} and name '{}'".format(
            resp.group.identifier, resp.group.name
        )
    )


@group.command("close")
@click.argument("identifiers", nargs=-1, required=True)
@click.pass_obj
def group_close(ctx, identifiers: List[str]) -> None:
    """Close/seal an existing group.

    \f

    :param ctx: Click context holding group-level parameters
    :param identifiers: The group ID(s) to seal
    """

    for identifier in identifiers:
        resp: GroupCreationResponse = ctx["client"].seal_group(group_id=identifier)
        write_or_print(
            "Closed group with ID {} and name '{}'".format(
                resp.group.identifier, resp.group.name
            )
        )


@analysis.command("list")
@click.option(
    "--number",
    default=5,
    type=click.IntRange(min=1, max=100),  # ~ 5 requests à 20 entries
    show_default=True,
    help="The number of most recent analysis jobs to display",
)
@click.pass_obj
def analysis_list(ctx, number: int) -> None:
    """Get a list of submitted analyses.

    \f

    :param ctx: Click context holding group-level parameters
    :param number: The number of analysis jobs to display
    :return:
    """

    result = AnalysisListResponse(analyses=[], total=0)
    offset = 0
    while True:
        resp = ctx["client"].analysis_list(offset=offset)
        if not resp.analyses:
            break
        offset += len(resp.analyses)
        result.analyses.extend(resp.analyses)
        if len(result.analyses) >= number:
            break

    # trim result to desired result number
    LOGGER.debug(resp.total)
    result = AnalysisListResponse(analyses=result[:number], total=resp.total)
    write_or_print(FORMAT_RESOLVER[ctx["fmt"]].format_analysis_list(result))


@analysis.command("report")
@click.argument("uuids", default=None, nargs=-1)
@click.option(
    "--min-severity",
    type=click.Choice(["low", "medium", "high"]),
    help="Ignore SWC IDs below the designated level",
    default=None,
)
@click.option(
    "--swc-blacklist",
    type=click.STRING,
    help="A comma-separated list of SWC IDs to ignore",
    default=None,
)
@click.option(
    "--swc-whitelist",
    type=click.STRING,
    help="A comma-separated list of SWC IDs to include",
    default=None,
)
@click.pass_obj
def analysis_report(
    ctx,
    uuids: List[str],
    min_severity: Optional[str],
    swc_blacklist: Optional[List[str]],
    swc_whitelist: Optional[List[str]],
) -> None:
    """Fetch the report for a single or multiple job UUIDs.

    \f

    :param ctx: Click context holding group-level parameters
    :param uuids: List of UUIDs to display the report for
    :param min_severity: Ignore SWC IDs below the designated level
    :param swc_blacklist: A comma-separated list of SWC IDs to ignore
    :param swc_whitelist: A comma-separated list of SWC IDs to include
    :return:
    """

    issues_list: List[
        Tuple[DetectedIssuesResponse, Optional[AnalysisInputResponse]]
    ] = []
    formatter: BaseFormatter = FORMAT_RESOLVER[ctx["fmt"]]
    for uuid in uuids:
        resp = ctx["client"].report(uuid)
        inp = (
            ctx["client"].request_by_uuid(uuid)
            if formatter.report_requires_input
            else None
        )

        util.filter_report(
            resp,
            min_severity=min_severity,
            swc_blacklist=swc_blacklist,
            swc_whitelist=swc_whitelist,
        )
        resp.uuid = uuid
        issues_list.append((resp, inp))

    write_or_print(formatter.format_detected_issues(issues_list))
    sys.exit(ctx["retval"])


def get_analysis_info(
    client,
    uuid: str,
    min_severity: Optional[str],
    swc_blacklist: Optional[List[str]],
    swc_whitelist: Optional[List[str]],
) -> Tuple[AnalysisStatusResponse, DetectedIssuesResponse, AnalysisInputResponse]:
    """Fetch information related to the specified analysis job UUID.

    Given a UUID, this function will query the MythX API for the
    analysis status, the analysis' input data, and the issue report.
    Furthermore, filtering parameters can be passed to remove certain
    SWCs or severities from the returned report.
    """

    resp: DetectedIssuesResponse = client.report(uuid)
    inp: Optional[AnalysisInputResponse] = client.request_by_uuid(uuid)
    status: AnalysisStatusResponse = client.status(uuid)
    util.filter_report(
        resp,
        min_severity=min_severity,
        swc_blacklist=swc_blacklist,
        swc_whitelist=swc_whitelist,
    )
    # extend response with job UUID to keep formatter logic isolated
    resp.uuid = uuid

    return status, resp, inp


@cli.command()
@click.argument("target")
@click.option(
    "--template",
    "-t",
    "user_template",
    type=click.Path(exists=True),
    help="A custom report template",
    default=None,
)
@click.option("--aesthetic", is_flag=True, default=False, hidden=True)
@click.option(
    "--markdown", is_flag=True, default=False, help="Render the report as Markdown"
)
@click.option(
    "--min-severity",
    type=click.STRING,
    help="Ignore SWC IDs below the designated level",
    default=None,
)
@click.option(
    "--swc-blacklist",
    type=click.STRING,
    help="A comma-separated list of SWC IDs to ignore",
    default=None,
)
@click.option(
    "--swc-whitelist",
    type=click.STRING,
    help="A comma-separated list of SWC IDs to include",
    default=None,
)
@click.pass_obj
def render(
    ctx,
    target: str,
    user_template: str,
    aesthetic: bool,
    markdown: bool,
    min_severity: Optional[str],
    swc_blacklist: Optional[List[str]],
    swc_whitelist: Optional[List[str]],
) -> None:
    """Render an analysis job or group report as HTML.

    \f
    :param ctx: Click context holding group-level parameters
    :param target: Group or analysis ID to fetch the data for
    :param user_template: User-defined template string
    :param aesthetic: DO NOT TOUCH IF YOU'RE BORING
    :param markdown: Flag to render a markdown report
    :param min_severity: Ignore SWC IDs below the designated level
    :param swc_blacklist: A comma-separated list of SWC IDs to ignore
    :param swc_whitelist: A comma-separated list of SWC IDs to include
    """

    client: Client = ctx["client"]

    default_template = DEFAULT_MD_TEMPLATE if markdown else DEFAULT_HTML_TEMPLATE
    # enables user to include library templates in their own
    template_dirs = [default_template.parent]

    if user_template:
        user_template = Path(user_template)
        template_name = user_template.name
        template_dirs.append(user_template.parent)
    else:
        template_name = default_template.name

    env_kwargs = {
        "trim_blocks": True,
        "lstrip_blocks": True,
        "keep_trailing_newline": True,
    }
    if not markdown:
        env_kwargs = {
            "trim_blocks": True,
            "lstrip_blocks": True,
            "keep_trailing_newline": True,
        }
        if aesthetic:
            template_name = "aesthetic.html"

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dirs), **env_kwargs
    )
    template = env.get_template(template_name)

    issues_list: List[
        Tuple[
            AnalysisStatusResponse,
            DetectedIssuesResponse,
            Optional[AnalysisInputResponse],
        ]
    ] = []
    if len(target) == 24:
        # identified group
        list_resp = client.analysis_list(group_id=target)
        offset = 0
        while len(list_resp.analyses) < list_resp.total:
            offset += len(list_resp.analyses)
            list_resp.analyses.extend(
                client.analysis_list(group_id=target, offset=offset)
            )

        for analysis_ in list_resp.analyses:
            click.echo("Fetching report for analysis {}".format(analysis_.uuid))
            status, resp, inp = get_analysis_info(
                client=client,
                uuid=analysis_.uuid,
                min_severity=min_severity,
                swc_blacklist=swc_blacklist,
                swc_whitelist=swc_whitelist,
            )
            issues_list.append((status, resp, inp))
    elif len(target) == 36:
        # identified analysis UUID
        click.echo("Fetching report for analysis {}".format(target))
        status, resp, inp = get_analysis_info(
            client=client,
            uuid=target,
            min_severity=min_severity,
            swc_blacklist=swc_blacklist,
            swc_whitelist=swc_whitelist,
        )
        issues_list.append((status, resp, inp))
    else:
        raise click.UsageError(
            "Invalid target. Please provide a valid group or analysis job ID."
        )

    rendered = template.render(issues_list=issues_list, target=target)
    if not markdown:
        rendered = htmlmin.minify(rendered, remove_comments=True)

    write_or_print(rendered, mode="w+")


@cli.command()
@click.pass_obj
def version(ctx) -> None:
    """Display API version information.

    \f

    :param ctx: Click context holding group-level parameters
    :return:
    """

    resp = ctx["client"].version()
    write_or_print(FORMAT_RESOLVER[ctx["fmt"]].format_version(resp))


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
