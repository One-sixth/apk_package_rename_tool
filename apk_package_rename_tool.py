'''
APK修改包名快捷工具
注意，对自带验证的包和Kotlin包可能无效。
你需要预先安装jre
'''

import subprocess
import os
import glob
import lxml.etree as et
import shutil
import argparse


root_dir = os.path.abspath('.')


# 预定义路径常量
JAVA_PATH = 'java'
apktool_path = f'{root_dir}/utils/apktool_2.4.1.jar'
signapk_path = f'{root_dir}/utils/signapk.jar'
pem_path = f'{root_dir}/utils/testkey.x509.pem'
pk8_path = f'{root_dir}/utils/testkey.pk8'
tmp_dir = f'{root_dir}/tmp'


def replace_all_str_file_or_dir(file_or_dir, wait_replace_str, target_replace_str, suffix='*'):
    '''
    替换目标目录下所有符合要求的文件的指定内容
    :param file_or_dir:
    :param wait_replace_str:
    :param target_replace_str:
    :param suffix:
    :return:
    '''
    if os.path.isdir(file_or_dir):
        files = glob.glob(f'{file_or_dir}/**/*.{suffix}', recursive=True)
    elif os.path.isfile(file_or_dir):
        files = [file_or_dir]
    else:
        print(f'{file_or_dir} 不是一个文件或文件夹')
        raise AssertionError()

    wait_replace_str = bytes(wait_replace_str, 'utf8')
    target_replace_str = bytes(target_replace_str, 'utf8')

    for p in files:
        text: bytes = open(p, 'rb').read(-1)
        if text.find(wait_replace_str) != -1:
            print('已替换', p)
            text = text.replace(wait_replace_str, target_replace_str)
            open(p, 'wb').write(text)


def is_valid_package_name(name):
    # 检查是否为有效包名
    b = len(name) > 1
    valid_char = list(range(ord('a'), ord('z')+1)) + list(range(ord('A'), ord('Z')+1)) + [ord('.')]
    valid_char = [chr(i) for i in valid_char]
    b = b and name[0] in valid_char[:-1]
    b = b and set(name).issubset(valid_char)
    return b


def package_rename(input_apk_path, new_package_name):
    SRC_APK = input_apk_path
    DST_PACKAGE_NAME = new_package_name
    dst_package_local = DST_PACKAGE_NAME.replace('.', '/')

    # 第一步，解包
    print('解包中')
    out_apk_name = DST_PACKAGE_NAME
    apk_unpack_dir = f'{tmp_dir}/{out_apk_name}'
    shutil.rmtree(apk_unpack_dir, ignore_errors=True)
    os.makedirs(apk_unpack_dir)

    unpack_cmd = f'{JAVA_PATH} -jar {apktool_path} -f d {SRC_APK} -o {apk_unpack_dir}'
    print(unpack_cmd)
    try:
        subprocess.run(unpack_cmd, check=True)
    except subprocess.CalledProcessError:
        print('apktool 解包失败。请检查java是否已安装，apktool是否版本过低，或apk文件是否存在')
        exit()


    # 读取原包名信息和移动位置
    info_path = f'{apk_unpack_dir}/AndroidManifest.xml'
    xml_tree = et.parse(info_path)
    ori_package_name = str(xml_tree.getroot().attrib['package'])
    ori_package_local = ori_package_name.replace('.', '/')

    wait_move_dir = f'{apk_unpack_dir}/smali/{ori_package_local}'
    new_move_dir = f'{apk_unpack_dir}/smali/{dst_package_local}'

    shutil.move(wait_move_dir, new_move_dir)


    # 改名
    # 先改名表单
    replace_all_str_file_or_dir(info_path, ori_package_name, DST_PACKAGE_NAME)
    # 然后改名smali
    smali_path = f'{apk_unpack_dir}/smali'
    replace_all_str_file_or_dir(smali_path, ori_package_name, DST_PACKAGE_NAME, 'smali')
    replace_all_str_file_or_dir(smali_path, ori_package_local, dst_package_local, 'smali')

    # 重命名xml的内容，这个一般不使用
    # xml_path = f'{apk_unpack_dir}/res'
    # helper.replace_all_str_file_or_dir(xml_path, ori_package_name, DST_PACKAGE_NAME, '.xml')


    # 改完了，现在开始打包
    out_apk_path = f'{tmp_dir}/{DST_PACKAGE_NAME}.apk'
    pack_cmd = f'{JAVA_PATH} -jar {apktool_path} -f b {apk_unpack_dir} -o {out_apk_path}'
    try:
        subprocess.run(pack_cmd, check=True)
    except subprocess.CalledProcessError:
        print('apktool 打包失败。请检查java是否已安装，apktool是否版本过低，或apk文件是否存在')
        exit()


    # 打包完成，现在加上签名
    out_apk_sign_path = f'{tmp_dir}/{DST_PACKAGE_NAME}_sign.apk'
    sign_cmd = f'{JAVA_PATH} -jar {signapk_path} {pem_path} {pk8_path} {out_apk_path} {out_apk_sign_path}'
    try:
        subprocess.run(sign_cmd, check=True)
    except subprocess.CalledProcessError:
        print('signapk 签名失败。请检查java是否已安装，signapk是否版本过低，或apk文件是否存在')
        exit()

    print('改包名完成，输出文件位于', out_apk_sign_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='简单的APK包名重命名工具')
    parser.add_argument('-i', '--input', required=True, type=str, help='指定输入APK的路径')
    parser.add_argument('-n', '--name', required=True, type=str, help='新的包名')

    args = parser.parse_args()
    if not is_valid_package_name(args.name):
        print('错误！无效包名', args.name)
        exit(-1)

    if not os.path.isfile(args.input):
        print('错误！输入文件不存在或不是一个有效文件', args.input)
        exit(-1)

    package_rename(args.input, args.name)
