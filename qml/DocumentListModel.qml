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
        model: documentListModel
        width: parent.width; height: parent.height - button_height()
        anchors.top: buttonRow.bottom

        delegate: Component {

            Rectangle {
                id: listrect
                color: "darkgray"
                width: pythonList.width; height: documentText.paintedHeight + 10

                Rectangle {
                    id: versrect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: documentText.paintedHeight + 10; radius: 6

                    Text {
                        id: documentText
                        wrapMode: Text.Wrap
                        text: model.documentItem.filename
                        color: "white"
                        width: parent.width
                        font.pointSize: 13
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left; right: parent.right;
                            leftMargin: 5
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.clicked(documentListModel, model.documentItem) }
                    }
                }
            }
        }
    }
}
