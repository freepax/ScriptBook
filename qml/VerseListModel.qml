import Qt 4.7


Item {

    NavigationButtons {
        id: buttonRow
        z: 1
        anchors.top: parent.top
        width: parent.width; height: button_height()
        onButtonClicked: buttonController.buttonClicked(button)
    }

    ListView {
        id: pythonList
        model: verseListModel
        width: parent.width; height: parent.height - buttonRow.button_height()
        anchors.top: buttonRow.bottom

        delegate: Component {

            Rectangle {
                id: listrect
                color: "darkgray"
                width: pythonList.width; height: verseText.paintedHeight + 10

                Rectangle {
                    id: versrect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: verseText.paintedHeight + 10; radius: 6

                    Text {
                        id: verseText
                        wrapMode: Text.Wrap
                        text: model.verseItem.text
                        color: "white"
                        width: parent.width - 10
                        font.pointSize: 10
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left; right: parent.right;
                            leftMargin: 5
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.clicked(verseListModel, model.verseItem) }
                    }
                }
            }
        }
    }
}
