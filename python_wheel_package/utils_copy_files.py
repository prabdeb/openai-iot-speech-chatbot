import os
import shutil
import sys

def copy_python_files_from_azure_iot_modules(azure_iot_solution_path: str = "../azure_iot_solution") -> None:
    """
    Copy all python files from azure_iot_solution_path folder to utils folder
    :param module_path: path to azure_iot_solution_path folder
    :return: None
    """

    for root, dirs, files in os.walk(f"{azure_iot_solution_path}/modules"):
        for dir in dirs:
            if dir == "__pycache__":
                continue
            for root2, dirs2, files2 in os.walk(f"{root}/{dir}"):
                for file in files2:
                    if file.endswith(".py"):
                        print(f"Copying {root2}/{file} to ./openai_iot/{dir}/{file}")
                        shutil.copy(f"{root2}/{file}", f"./openai_iot/{dir}/{file}")
                for dir2 in dirs2:
                    if dir2 == "__pycache__":
                        continue
                    for root3, dirs3, files3 in os.walk(f"{root2}/{dir2}"):
                        for file in files3:
                            if file.endswith(".txt"):
                                print(f"Copying {root3}/{file} to ./openai_iot/{dir}/{dir2}/{file}")
                                shutil.copy(f"{root3}/{file}", f"./openai_iot/{dir}/{dir2}/{file}")

def delete_copied_files_from_openai_iot(open_ai_iot_path: str = "./openai_iot") -> None:
    """
    Delete all python files from openai_iot folder
    :param open_ai_iot_path: path to openai_iot folder
    :return: None
    """

    for root, dirs, files in os.walk(open_ai_iot_path):
        for dir in dirs:
            for root2, dirs2, files2 in os.walk(f"{root}/{dir}"):
                for file in files2:
                    if file.endswith(".py") and file != "__init__.py":
                        print(f"Deleting {root2}/{file}")
                        os.remove(f"{root2}/{file}")
                for dir2 in dirs2:
                    for root3, dirs3, files3 in os.walk(f"{root2}/{dir2}"):
                        for file in files3:
                            if file.endswith(".txt"):
                                print(f"Deleting {root3}/{file}")
                                os.remove(f"{root3}/{file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments. Use copy or delete")
        exit(1)
    if sys.argv[1] == "copy":
        copy_python_files_from_azure_iot_modules()
    elif sys.argv[1] == "delete":
        delete_copied_files_from_openai_iot()
    else:
        print("Wrong argument. Use copy or delete")
