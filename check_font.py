import os

# 'font' 폴더의 전체 경로 (game.py는 'font' 폴더를 사용)
# os.path.join은 현재 폴더 경로와 'font'를 합쳐서 완전한 경로로 만들어줍니다.
font_dir = os.path.join(os.getcwd(), 'font')

print(f"'{font_dir}' 폴더에서 폰트 파일을 찾습니다...")
print("-" * 40)

try:
    # 'font' 폴더에 있는 파일 목록을 가져옵니다.
    files_in_dir = os.listdir(font_dir)

    if not files_in_dir:
        print("결과: 'font' 폴더가 비어있습니다.")
        print("      인터넷에서 한글 폰트(ttf 파일)를 다운로드해서 'font' 폴더에 넣어주세요.")
    else:
        print("결과: 아래 파일들을 찾았습니다.")
        found_font = False
        for filename in files_in_dir:
            if filename.lower().endswith(('.ttf', '.otf')):
                print(f"  -> {filename} (폰트 파일)")
                found_font = True
            else:
                print(f"  -> {filename} (폰트 파일이 아님)")

        print("-" * 40)
        if found_font:
            print("위 목록에서 '.ttf' 또는 '.otf'로 끝나는 폰트 파일 이름을 복사해서 알려주세요!")
        else:
            print("폰트 파일(.ttf 또는 .otf)이 없습니다. 'font' 폴더에 넣어주세요.")

except FileNotFoundError:
    print("오류: 'font' 폴더를 찾을 수 없습니다.")
    print("      'main.py'가 있는 곳에 'font'라는 이름의 폴더를 만들어주세요.")

print("-" * 40)
input("확인이 끝났으면 Enter 키를 눌러 창을 닫으세요...")