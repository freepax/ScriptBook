import Qt 4.7


Rectangle {
    id: root
    color: "black"
    ScriptBookGradients { id: cg }

    property alias hostText: hostEdit.inputText
    property alias portText: portEdit.inputText

    /// Emit the model.connectSignal with host name and port number
    function connect_to_server() {
        ftpController.connectSignal(hostEdit.inputText, portEdit.inputText)
    }

    /// Grid element with
    function gridElementWidth() {
        return root.width / 2
    }

    /// Grid element height
    function gridElementHeight() {
        return 40
    }

    /// Hostname text label
    TextLabel {
        id: textLabel
        gradient: cg.onn;
        height: gridElementHeight(); width: gridElementWidth();
        text: "Host"; textColor: "white"; borderColor: "black"; borderWidth: 2
        anchors.top: root.top; anchors.left: root.left
    }

    /// Hostname line edit
    LineEdit {
        id: hostEdit
        gradient: cg.gray;
        Component.onCompleted: { textColor = "white"; set_focus() }
        width: gridElementWidth(); height: gridElementHeight(); radius: 4
        border.color: "black"; border.width: 2
        KeyNavigation.tab: portEdit.focusItem
        onSendMessage: connect_to_server()
        anchors.top: root.top; anchors.right: root.right
    }

    /// Port number text label
    TextLabel {
        id: portLabel
        gradient: cg.onn;
        height: gridElementHeight(); width: gridElementWidth();
        text: "Port"; textColor: "white"; borderColor: "black"; borderWidth: 2
        anchors.top: textLabel.bottom; anchors.left: root.left
    }

    /// Port number line edit
    LineEdit {
        id: portEdit
        gradient: cg.gray
        Component.onCompleted: { textColor = "white"; set_focus() }
        width: gridElementWidth(); height: gridElementHeight(); radius: 4
        border.color: "black"; border.width: 2
        KeyNavigation.tab: hostEdit.focusItem
        onSendMessage: connect_to_server()
        anchors.top: hostEdit.bottom; anchors.right: root.right
    }


    PushButton {
        id: cancelButton
        text: "Cancel"; textColor: "steelblue"
        width: gridElementWidth(); height: gridElementHeight(); radius: 4
        border.color: "black"; border.width: 2
        KeyNavigation.tab: hostEdit.focusItem
        onTrigger: ftpController.cancelSignal()
        anchors.bottom: root.bottom; anchors.left: root.left
    }

    PushButton {
        id: connectButton
        text: "Connect"; textColor: "steelblue"
        width: gridElementWidth(); height: gridElementHeight(); radius: 4
        border.color: "black"; border.width: 2
        KeyNavigation.tab: hostEdit.focusItem
        onTrigger: connect_to_server()
        anchors.bottom: root.bottom; anchors.right: root.right
    }

}