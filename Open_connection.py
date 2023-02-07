import paramiko

def get_connection():
    """
    Connects to ssh of homeserver
    """

    ssh = paramiko.SSHClient()

    ssh.connect(hostname="10.0.0.196", username="luigi", password="123456")

    sftp = ssh.open_sftp()

    return sftp

