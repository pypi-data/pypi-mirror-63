import subprocess


def run(cmd: str):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8"), error.decode("utf-8")
