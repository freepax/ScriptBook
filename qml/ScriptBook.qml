import Qt 4.7

Rectangle {
    id: mainWindow
    color: "darkgreen"

    width: 100; height: 100

    Component.onCompleted: console.log("height width", height, width)

    function buttonWidth() {
        return mainWindow.width / 4
    }

    function buttonHeight() {
        return buttonWidth < 40 ? 40 : buttonWidth()
    }

    Column {
        anchors.fill: parent

        Rectangle {
            color: "black"
            width: mainWindow.width; height: buttonHeight()
            Row {
                anchors.fill: parent
                Rectangle { width: buttonWidth(); height: buttonHeight(); color: "red"; radius: 2 }
                Rectangle { width: buttonWidth(); height: buttonHeight(); color: "blue"; radius: 2 }
                Rectangle { width: buttonWidth(); height: buttonHeight(); color: "gray"; radius: 2 }
                Rectangle { width: buttonWidth(); height: buttonHeight(); color: "green"; radius: 2 }
            }
        }

        BookListModel {
            id: bookList
            width: mainWindow.width; height: mainWindow.height - buttonHeight()
            Component.onCompleted: {
                console.log("BookListModel", height, width)
            }
            model: bookListModel
        }
    }
}

