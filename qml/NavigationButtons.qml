import QtQuick 1.0


Rectangle {
    id: buttonBox
    //color: "yellow"

    function button_height() {
        return 40
    }

    function button_width() {
        return width / 5
    }


    property int buttonNumber: 0
    property color textColor: "white"
    signal buttonClicked(int button)

    ScriptBookGradients { id: gr }


    onButtonNumberChanged: {
        set_gradient(buttonNumber)
        console.log("NavigationButton.qml: buttonNumber ", buttonNumber)
    }

    /// Set/reset gradient on buttons
    function set_gradient(button) {

        /// Check button range
        if (button < 0 || button > 4) {
            console.log("NavigationButtons.qml::set_gradient Unknown button")
            return
        }

        /// The document button
        if (button == 0) {
            documentButton.gradient = gr.off
            console.log("NavigationButtons.qml::set_gradient DOCUMENT BUTTON")
        }
        else
            documentButton.gradient = gr.onn

        if (button == 1) {
            bookButton.gradient = gr.off
            console.log("NavigationButtons.qml::set_gradient BOOK BUTTON")
        }
        else
            bookButton.gradient = gr.onn

        if (button == 2) {
            chapterButton.gradient = gr.off
            console.log("NavigationButtons.qml::set_gradient CHAPTER BUTTON")
        }
        else
            chapterButton.gradient = gr.onn

        if (button == 3) {
            versButton.gradient = gr.off
            console.log("NavigationButtons.qml::set_gradient VERSE BUTTON")
        }
        else
            versButton.gradient = gr.onn

        if (button == 4) {
            settingsButton.gradient = gr.off
            console.log("NavigationButtons.qml::set_gradient SETTINGS BUTTON")
        }
        else
            settingsButton.gradient = gr.onn
    }

    Row {
        PushButton { /// Gets you back to all the documents
            id: documentButton
            gradient: gr.onn
            text: "Docs"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(0)
        }

        PushButton { /// Gets you back to the books in the opened document
            id: bookButton
            gradient: gr.onn
            text: "Books"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(1)
        }

        PushButton { /// Gets you back to the chapter in the book
            id: chapterButton
            gradient: gr.onn
            text: "Chapt"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(2)
        }

        PushButton { /// Gets you back to the chapter in the book
            id: versButton
            gradient: gr.onn
            text: "Vers"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(3)
        }

        PushButton { /// Show more options
            id: settingsButton
            gradient: gr.onn
            text: "Tools"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(4)
        }
    }
}
