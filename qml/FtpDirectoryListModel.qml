import Qt 4.7


Item {
    id: root

    property int buttonHeight: 40

    ScriptBookGradients { id: cg }


    ListView {
        id: pythonList
        model: directoryListModel
        width: parent.width; height: parent.height - root.buttonHeight
        anchors.top: root.top

        delegate: Component {

            Rectangle {
                id: listrect
                width: pythonList.width; height: 40; color: "steelblue"

                Rectangle {
                    id: directoryrect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: root.width; height: 40; radius: 6

                    Text {
                        id: diretoryText
                        text: model.directoryItem.directoryname
                        color: "white"
                        width: parent.width - 10
                        font.pointSize: 14
                        anchors.centerIn: directoryrect
                    }

                    MouseArea {
                        anchors.fill: directoryrect
                        onClicked: { controller.clicked(directoryListModel, model.directoryItem) }
                    }
                } /// directoryrect

            }

        }
    } /// component


    PushButton {
        id: cancelButton
        //z: 1
        text: "Cancel"; textColor: "steelblue"
        width: root.width; height: root.buttonHeight; radius: 4
        border.color: "black"; border.width: 2
        anchors.top: pythonList.bottom
        onTrigger: ftpController.cancelSignal()
    }

} /// item
