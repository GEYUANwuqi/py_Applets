import subprocess
import shutil

print("文件请放在源码路径下...\n")

# 定义要写入的.bat文件的路径
bat_file_path = "/go.bat"
pic_name=input("请输入文件名称(不带文件后缀)：")+".png"
out_pic_name=input("请输入输出文件名(不带文件后缀)：")+".png"
# 清空.bat文件的内容并写入新内容
with open(bat_file_path, "w") as f:
    # 假设要填入的变量是variable
    variable = f"realesrgan-ncnn-vulkan.exe -i {pic_name} -o {out_pic_name} -n realesrgan-x4plus-anime"
    bat=variable
    # 写入.bat文件的新内容，可以根据需要调整
    f.write(f"{bat}")

# 运行更新后的.bat文件
subprocess.run([bat_file_path], shell=True)

#源目录——级目录
y_file =out_pic_name
x_file=pic_name
target_folder = input("请输入存放照片的文件路径：")

# 移动文件到目标文件夹
shutil.move(y_file, target_folder)
shutil.move(x_file, target_folder)

input("一键程序运行完毕,请查看文件夹内的文件(任意键退出)...")
