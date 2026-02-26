import zipfile
import os
import datetime


def export_project():
    # 1. 定义生成的压缩包名字 (加上时间戳，防止搞混)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    zip_filename = f"智能体后端交付包_{timestamp}.zip"

    # 2. 定义你需要打包的“白名单”文件
    # 只有在这个列表里的文件才会被打包，其他的垃圾文件一律不要
    files_to_pack = [
        "main.py",
        "core.py",
        "personas.py",
        "config.py",
        "allcomments_with_label_processed.csv",  # 你的数据源
        "simulation_result.json"  # 你的运行结果
    ]

    print(f"📦 正在打包到: {zip_filename} ...")

    # 3. 开始压缩
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            found_count = 0
            for file in files_to_pack:
                if os.path.exists(file):
                    zf.write(file)
                    print(f"  ✅ 已添加: {file}")
                    found_count += 1
                else:
                    print(f"  ⚠️ 文件缺失 (跳过): {file}")

            # 再写一个自动生成的 Readme
            readme_content = """
【智能体仿真后端代码】
1. 安装依赖: pip install pandas openai
2. 运行入口: main.py
3. 结果文件: simulation_result.json (可直接用于前端展示)
            """
            zf.writestr("使用说明.txt", readme_content)
            print("  ✅ 已添加: 使用说明.txt")

        print("-" * 30)
        if found_count > 0:
            print(f"🎉 打包成功！请把桌面上的【{zip_filename}】发给队友即可。")
        else:
            print("❌ 打包失败：一个文件都没找到，请检查你是否在项目根目录下运行。")

    except Exception as e:
        print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    export_project()