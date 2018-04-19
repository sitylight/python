import fileinput
import re


class UpdateDatabaseInfo:
    file_path = ''
    ip_address = ''
    port = ''
    database = ''
    username = ''

    def __init__(self, file_path, ip_address, port, database, username):
        self.file_path = file_path
        self.ip_address = ip_address
        self.port = port
        self.database = database
        self.username = username

    def updateTomcat(self):
        file_data = ''
        regex = '"(.*)"'
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if 'dataSource.user' in line:
                    line = re.sub(regex, '"' + self.username + '"', line)
                elif 'dataSource.serverName' in line:
                    line = re.sub(regex, '"' + self.ip_address + '"', line)
                elif 'dataSource.portNumber' in line:
                    line = re.sub(regex, '"' + self.port + '"', line)
                elif 'dataSource.databaseName' in line:
                    line = re.sub(regex, '"' + self.database + '"', line)
                file_data += line
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(file_data)
        print('tomcat database info is updated')

    def updateJetty(self):
        file_data = ''
        regex = '>(.*)<'
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if 'jdbcUrl' in line:
                    line = re.sub(regex,
                                  '>jdbc:postgresql://' + self.ip_address + ':' + self.port + '/' + self.database + '<',
                                  line)
                elif 'username' in line:
                    line = re.sub(regex, '>' + self.username + '<', line)
                file_data += line
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(file_data)
        print('jetty database info is updated')

    def updateTask(self):
        file_data = ''
        regex = '=[a-z:/\d_\.]+'
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if 'resource.ds1.jdbcUrl' in line:
                    if '#' not in line:
                        print(
                            'new value:' + '=jdbc:postgresql://' + self.ip_address + ':' + self.port + '/' + self.database)
                        line = re.sub(regex,
                                      '=jdbc:postgresql://' + self.ip_address + ':' + self.port + '/' + self.database,
                                      line)
                elif 'resource.ds1.xaProperties.user' in line:
                    line = re.sub(regex, '=' + self.username, line)
                file_data += line
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(file_data)
        print('task database info is updated')


if __name__ == '__main__':
    context_path = 'C:\\cbxsoftware\\apache-tomcat-8.0.47\\conf\\context.xml'
    jetty_path = 'C:\cbxsoftware\cbx-develop\cbx-biz\settings\jetty9env.xml'
    task_path = 'C:\cbxsoftware\cbx-develop\cbx-biz\\task\DBSetting.properties'
    ip_address = '192.168.5.132'
    # ip_address = 'localhost'
    # ip_address = '192.168.1.105'

    port = '5432'
    database = 'cbx6_u_3'
    username = 'postgres'

    info = UpdateDatabaseInfo(context_path, ip_address, port, database, username)
    info.updateTomcat()
    info.file_path = jetty_path
    info.updateJetty()
    info.file_path = task_path
    info.updateTask()
