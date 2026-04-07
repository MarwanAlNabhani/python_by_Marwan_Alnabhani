import paramiko 

def ssh_connect(hostname, username, password):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the server
        ssh.connect(hostname, username=username, password=password)
        print(f"Successfully connected to {hostname}")
        
        # Execute a command (optional)
        stdin, stdout, stderr = ssh.exec_command('ls -l')
        print(stdout.read().decode())
        
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        ssh.close() 

if __name__ == "__main__":
    hostname = input("Enter the hostname or IP address: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    
    ssh_connect(hostname, username, password)
