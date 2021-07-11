from sys import stdout

import decouple
from paramiko import SSHClient
from scp import SCPClient

HOME = decouple.config("HOME")
HOST = decouple.config("HOST")
PORT = int(decouple.config("PORT"))
USER = decouple.config("USERNAME")
RSA_KEY = f'{HOME}/{decouple.config("RSA_KEY")}'


# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    stdout.write(
        "%s's progress: %.2f%%   \r" % (filename, float(sent) / float(size) * 100)
    )


def copy_file(local_file, remote_file):
    while True:
        try:

            with SSHClient() as ssh:
                ssh.load_system_host_keys()
                ssh.connect(
                    hostname=HOST, port=PORT, username=USER, key_filename=RSA_KEY
                )

                with SCPClient(ssh.get_transport(), progress=progress) as scp:
                    scp.put(local_file, remote_path=remote_file)
                return

        except Exception as e:
            print(e)
