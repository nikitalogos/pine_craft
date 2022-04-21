import os


def make_dir_with_user_ask(dir_path):
    if os.path.exists(dir_path):
        print(f'{dir_path} exists! Do you want to overwrite it? y/n:')
        while True:
            inp = input()
            if inp == 'n':
                print('Abort!')
                exit(0)
            elif inp == 'y':
                break
            else:
                print('Invalid choice. Please type y or n:')
                continue
    else:
        os.makedirs(dir_path)
