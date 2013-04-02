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
                width: pythonList.width; height: versText.paintedHeight + 10; color: "darkgreen"

                Rectangle {
                    id: chapterRect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: versText.paintedHeight + 10; radius: 6

                    Text {
                        id: chapterText
                        text: model.chapterItem.no
                        color: "white"
                        width: 30
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: chapterRect.left; right: versText.left; leftMargin: 5
                        }
                    }

                    Text {
                        id: versText
                        //elide: Text.ElideRight
                        wrapMode: Text.Wrap
                        text: model.chapterItem.text
                        color: "white"
                        width: parent.width - 30
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: chapterText.right; right: chapterRect.right; rightMargin: 5
                        }
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

