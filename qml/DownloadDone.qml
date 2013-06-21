import QtQuick 1.0


Item {
    id: root

    ScriptBookGradients { id: cg }

    Component.onCompleted: { console.log("ROOT HEGHT", root.height, "WIDTH", root.width) }

    property int buttonHeight: 40

    function element_height() {
        return (root.height - root.buttonHeight - buttonRow.button_height())
    }


    NavigationButtons {
        id: buttonRow
        z: 1
        height: button_height(); width: root.width;
        onButtonClicked: buttonController.buttonClicked(button)
        anchors.top: root.top
    }

    Rectangle {
        id: label
        height: element_height(); width: root.width
        color: "#111"; border.color: "black"; border.width: 2
        anchors { top: buttonRow.bottom }

        Column {
            id: col
            anchors.centerIn: label

            Text {
                id: t1;
                width: label.width
                text: "Download Done"; color: "white";
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                id: t2;
                width: label.width
                text: "Click to load document"; color: "white";
                horizontalAlignment: Text.AlignHCenter
            }
        }

        MouseArea { onClicked: buttonController.buttonClicked(12); anchors.fill: label }
    }

    /// Download Done Button
    PushButton {
        id: doneButton
        height: root.buttonHeight; width: root.width; radius: 4
        text: "Back"; textColor: "steelblue"; gradient: cg.onn
        border.color: "black"; border.width: 2
        onTrigger: buttonController.buttonClicked(10)
        anchors { top: label.bottom }
    }
}
