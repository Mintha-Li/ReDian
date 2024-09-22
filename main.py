import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog 
from Ui_main import Ui_MainWindow
from pathlib import Path 
import func
import subprocess 
  
class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        self.ui = Ui_MainWindow()  
        self.ui.setupUi(self)
        self.fileNames=[]
  
        # 这里可以添加其他初始化代码  
        self.ui.selectFilesButton.clicked.connect(self.onPressedSelectFilesButton)
        self.ui.processButton.clicked.connect(self.onPressedProcessFilesButton)

    def onPressedSelectFilesButton(self):
        options = QFileDialog.Options()  
        fileNames, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",  
                                                   "CSV Files (*.csv);", options=options) 
        self.fileNames = fileNames
        self.ui.lineEditFiles.setText(str(fileNames))
        self.ui.labelFilesNum.setText(f"共{len(fileNames)}个文件")

    def onPressedProcessFilesButton(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "选择保存文件夹", "/")  
        if folder_selected:  
            func.process_files(file_names=self.fileNames,
                            output_folder=folder_selected,
                            platforms=['微博', '知乎', '抖音'],
                            num_ranks=3) 
            open_folder_in_explorer(folder_selected)

def open_folder_in_explorer(folder_path):  
    if sys.platform.startswith('win'):  
        path_with_backslashes = str(folder_path).replace('/', '\\')  
        subprocess.Popen(f'explorer {path_with_backslashes}', shell=True)
    elif sys.platform.startswith('darwin'):  
        subprocess.run(['open', '-R', folder_path], check=True)  
    else:  
        # 假设大多数Linux发行版都支持xdg-open  
        subprocess.run(['xdg-open', folder_path], check=True) 

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    main_window = MainWindow()  
    main_window.show()  
    sys.exit(app.exec_())