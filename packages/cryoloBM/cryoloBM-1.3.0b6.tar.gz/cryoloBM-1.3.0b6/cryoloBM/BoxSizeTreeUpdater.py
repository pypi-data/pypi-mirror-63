from PyQt5.QtCore import (QThread, pyqtSignal, QObject)
import os

class BoxSizeTreeUpdater(QThread):

    started = pyqtSignal()
    finished= pyqtSignal()

    def __init__(self,boxmanager):
        self.boxmanager = boxmanager
        self.update_current = False
        self.exiting = False
        super(BoxSizeTreeUpdater, self).__init__()

    def __del__(self):

        self.exiting = True
        self.wait()

    def update(self):
        self.started.emit()


        def update(boxes, item):
            res = list(map(lambda x: self.boxmanager.check_if_should_be_visible(x), boxes))
            num_box_vis = sum(res)

            item.setText(1, "{0:> 4d}  / {1:> 4d}".format(num_box_vis, len(res)))

        if self.update_current:
            item = self.boxmanager.tree.currentItem()
            filename = os.path.splitext(item.text(0))[0]
            update(self.boxmanager.box_dictionary[filename], item)

        else:
            root = self.boxmanager.tree.invisibleRootItem().child(0)
            child_count = root.childCount()
            for i in range(child_count):
                if self.exiting:
                    break
                item = root.child(i)
                filename = os.path.splitext(item.text(0))[0]
                if filename in self.boxmanager.box_dictionary:
                    update(self.boxmanager.box_dictionary[filename], item)

        self.finished.emit()
