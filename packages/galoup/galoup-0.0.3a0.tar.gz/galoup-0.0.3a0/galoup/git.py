from galoup import process
from galoup.error import ProcessError, NotYetImplementedError


def get_origin():
    output, error = process.run('git config --get remote.origin.url')
    if len(error) != 0:
        raise ProcessError("while trying to get git origin: " + error)
    output = output.rstrip()
    # SSH style
    if "@" in output:
        without_user = output.split("@", 1)[1]
        colon_split = without_user.split(':', 1)
        repo_provider, without_repo_provider = colon_split[0], "".join(colon_split[1:])
        repo_part = without_repo_provider.rsplit(".", 1)[0]
        return repo_provider, repo_part
    else:
        raise NotYetImplementedError("cannot handle non SSH git origins. Please implement to continue.")

