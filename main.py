print("starting betting predictor program")

#exec(open('dt_prompter.py').read())
import os
import args_parser

try:
    input_str = bool(int(args_parser.args_run))
except Exception as e:
    print(e)
    input_str = bool(int(input("run-script (1) or see-past-excel (0)?: ")))

if input_str:
    default2 = os.getcwd()
    print(default2)
    while args_parser.args_level <= 1:
        print("running raw-stats_downloader")
        exec(open('raw-stats_downloader.py').read())
        os.chdir(default2)
        break
    while args_parser.args_level <= 2:
        print("running espn-stats_downloader")
        exec(open('espn-stats_downloader.py').read())
        os.chdir(default2)
        break
    while args_parser.args_level <= 3:
        print("running results_data_extractor")
        exec(open('results_data_extractor.py').read())
        os.chdir(default2)
        break
    while args_parser.args_level <= 4:
        print("running fixture_data_extractor")
        exec(open('fixture_data_extractor.py').read())
        os.chdir(default2)
        break
    while args_parser.args_level <= 5:
        print("running docx-auto_editor")
        exec(open('docx-auto_editor.py').read())
        break
    print("ended betting predictor program")
else:
    default2 = os.getcwd()
    print("opening last bet folder to view it")
    print(default2)
    import glob
    globber = glob.glob("*", recursive=False)
    globber_recon = []
    for globby in globber:
        globby_path = os.path.join(default2,globby)
        if os.path.exists(globby_path):
            if os.path.isdir(globby_path):
                globber_recon.append(globby)
    globber = list(set(globber_recon))
    try:
        globber.remove('__pycache__')
        globber.remove('DATA-VIS')
    except ValueError:
        pass
    globber.sort()
    today_folder = os.path.join(default2,globber[-1])
    os.chdir(today_folder)
    print(today_folder)
    exec(open('excel-file-opener.py').read())
    exec(open('docx-file-opener.py').read())
    print("ended betting predictor program")
    os.chdir(default2)