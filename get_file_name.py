import os


def file_name(file_dir):
    f_list = os.listdir(file_dir)
    f_set = []
    for f in f_list:
        f_set.append(f.split('_')[0])
    modules = list(set(f_set))
    for m in modules:
        print(m)


if __name__ == '__main__':
    file_dir = 'C:\\Users\\derrick.liang\\Desktop\\excels\\rd2'
    file_name(file_dir)
