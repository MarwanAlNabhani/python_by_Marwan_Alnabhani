import os
import paramiko


def load_private_key(key_path, passphrase=None):
    if not os.path.isfile(key_path):
        raise FileNotFoundError(f"Private key file not found: {key_path}")

    for key_cls in (paramiko.RSAKey, paramiko.ECDSAKey, paramiko.Ed25519Key, paramiko.DSSKey):
        try:
            return key_cls.from_private_key_file(key_path, password=passphrase)
        except paramiko.PasswordRequiredException:
            raise
        except paramiko.SSHException:
            continue

    raise ValueError("Unable to load private key. Make sure the file is a valid RSA, ECDSA, ED25519, or DSA key.")


def ssh_connect(hostname, username, key_path, key_passphrase=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = load_private_key(key_path, key_passphrase)
        ssh.connect(hostname, username=username, pkey=key)

        print(f"Successfully connected to {hostname} using key authentication")

        stdin, stdout, stderr = ssh.exec_command('ls -l')
        print(stdout.read().decode())
        error_output = stderr.read().decode().strip()
        if error_output:
            print(f"Command error: {error_output}")

    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        ssh.close()


if __name__ == "__main__":
    hostname = input("Enter the hostname or IP address: ")
    username = input("Enter the username: ")
    key_path = input("Enter the path to your private key file (e.g. C:\\Users\\YourName\\.ssh\\id_rsa): ")
    key_passphrase = input("Enter the key passphrase (leave blank if none): ") or None

    ssh_connect(hostname, username, key_path, key_passphrase)
