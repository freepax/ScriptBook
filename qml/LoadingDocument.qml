import QtQuick 1.0


Rectangle {
    id: root
    color: "black"

    ScriptBookGradients { id: cg }

    /// Top menu buttoms
    NavigationButtons {
        id: buttonRow
        z: 1
        anchors.top: root.top
        width: parent.width; height: button_height()
        onButtonClicked: buttonController.buttonClicked(button)
    }

    /// Loading document text rectangle
    Rectangle {
        id: textLabel
        color: "#222";
        y: parent.height / 100 * 40
        height: 40; width: parent.width;
        Text { text: "Loading document"; color: "white"; anchors.centerIn: parent }
    }

    /// The progress bar
    ProgressBar {
        id: progressbar
        color: "steelblue"
        height: 40; width: parent.width
        minimum: 0; maximum: 100
        value: 40
        anchors.top: textLabel.bottom
    }

    /// Download Done Button
    PushButton {
        id: doneButton
        text: "Cancel"; textColor: "steelblue"; gradient: cg.onn
        width: root.width; height: 40; radius: 4
        border.color: "black"; border.width: 2
        onTrigger: buttonController.buttonClicked(11)
        anchors.top: textLabel.button; anchors.bottom: root.bottom;
    }
}
