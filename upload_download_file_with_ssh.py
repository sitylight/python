import paramiko
import os
import glob


# run 'pip install paramikoto' install 'paramiko' module
def buildWar():
    path = 'C:/cbxsoftware/cbx-develop/cbx-biz'
    os.chdir(path)
    os.system('mvn clean package -P full,dev -DskipTests')
    os.chdir(path + '/target')
    files = glob.glob('cbx-biz' + '*SNAPSHOT.war')
    for file in files:
        print('rename ' + file)
        os.rename(file, 'main.war')


if __name__ == '__main__':
    # New SSHClient
    ssh = paramiko.SSHClient()
    host = '192.168.5.132'
    port = 22
    username = 'root'
    password = '123'

    # Default accept unknown keys
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect
    ssh.connect(host, port=port, username=username, password=password)

    # Execute shell remotely
    # ssh.exec_command('cd /derrick')
    # stdin, stdout, stderr = client.exec_command("ls -alh")
    # print(stdout.read())

    sftp = ssh.open_sftp()
    # download remote file
    # sftp.get('/tmp/updateJson.txt', 'updateJson.log')
    # buildWar()
    sftp.put('C:/cbxsoftware/cbx-develop/cbx-biz/target/main.war', '/tmp/main.war')
    sftp.close()
    ssh.close()
