import Qt 4.7


Item {

    function button_height() {
        return 40
    }

    function button_width() {
        return width / 4
    }

    NavigationButtons {
        id: buttonRow
        anchors.top: parent.top
        width: parent.width; height: button_height()
        onButtonClicked: buttonController.buttonClicked(button)
    }

    ListView {
        id: pythonList
        model: chapterListModel
        width: parent.width; height: parent.height - button_height()
        anchors.top: buttonRow.bottom

        delegate: Component {

            Rectangle {
                width: pythonList.width; height: versText.paintedHeight + 40; color: "steelblue"

                Rectangle {
                    id: chapterRect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: versText.paintedHeight + 40; radius: 6

                    Text {
                        id: chapterText
                        text: "Chapter  " + model.chapterItem.no
                        color: "steelblue"
                        width: parent.width - 10; height: 30
                        font.pointSize: 11
                        anchors { horizontalCenter: parent.horizontalCenter; top: parent.top; }
                    }

                    Text {
                        id: versText
                        wrapMode: Text.Wrap
                        text: model.chapterItem.text
                        color: "white"
                        width: parent.width - 10
                        font.pointSize: 10
                        anchors { horizontalCenter: parent.horizontalCenter; top: chapterText.bottom }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.clicked(chapterListModel, model.chapterItem) }
                    }
                }
            }
        }
    }
}

