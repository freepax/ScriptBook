import QtQuick 1.0


Rectangle {
    id: button
    radius: 2; height: 50; width: 100; gradient: buttonIdleGradient
    border.color: "black"; border.width: 2

    signal trigger
    signal down
    signal up
    signal keyPressed (int key)

    property alias text: buttonText.text
    property alias textColor: buttonText.color
    property alias focusItem: button

    property bool autoGradient: true

    Keys.onPressed: {
        if (event.key == Qt.Key_Return) {
            button.trigger()
            button.keyPressed(event.key)
            event.accepted = true;
        }
        else {
            button.keyPressed(event.key)
        }
    }

    Gradient {
        id: buttonPressedGradient
        GradientStop { id: offfirst; position: 0.0; color: "lightsteelblue" }
        GradientStop { id: offsecond; position: 0.5; color: "lightsteelblue" }
        GradientStop { id: offthird; position: 0.5; color: "black" }
        GradientStop { id: offfourth; position: 1.0; color: "black" }
    }

    Gradient {
        id: buttonIdleGradient
        GradientStop { id: onfirst; position: 0.0; color: "steelblue" }
        GradientStop { id: onsecond; position: 0.5; color: "steelblue" }
        GradientStop { id: onthird; position: 0.5; color: "black" }
        GradientStop { id: onfourth; position: 1.0; color: "black" }
    }

    Text { id: buttonText; text: button.text; anchors.centerIn: parent }

    MouseArea {
        id: mouseArea
        anchors.fill: parent;

        /// When mouse button is pressed down
        onPressed: {
            if (autoGradient == true)
                button.gradient = buttonPressedGradient
            button.down()
        }

        /// When mouse button is released
        onReleased: {
            if (autoGradient == true)
                button.gradient = buttonIdleGradient
            button.up()
        }

        /// The 'click' behavior
        onClicked: button.trigger()
    }
}
