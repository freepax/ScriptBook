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
        model: bookListModel
        width: parent.width; height: parent.height - button_height()
        anchors.top: buttonRow.bottom

        delegate: Component {

            Rectangle {
                width: pythonList.width; height: 40; color: "darkgreen"

                Rectangle {
                    id: bookRect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: parent.height; radius: 6

                    Text {
                        id: entryText
                        width: 30;

                        text: model.bookItem.entry
                        color: "white"
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: bookRect.left
                            right: nameText.left
                            leftMargin: 5
                        }
                    }

                    Text {
                        id: nameText
                        width: bookRect.width - 60
                        elide: Text.ElideRight
                        text: model.bookItem.name
                        color: "white"
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: entryText.right
                            right: chaptersText.left
                        }
                    }

                    Text {
                        id: chaptersText
                        width: 30
                        horizontalAlignment: Text.AlignRight
                        text: model.bookItem.chapters
                        color: "white"
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: nameText.right
                            right: bookRect.right
                            rightMargin: 5
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.clicked(bookListModel, model.bookItem) }
                    }
                }
            }
        }
    }

}
