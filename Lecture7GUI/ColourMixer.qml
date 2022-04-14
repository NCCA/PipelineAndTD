import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Dialogs
import Qt.labs.platform

Window {
    width: 400
    height: 500
    visible: true
    title: qsTr("Jessica's Colour Mixer")
    GridLayout
    {
        anchors.fill: parent
        rows:   4
        columns:   2
        Rectangle{
            Layout.row : 0
            Layout.columnSpan : 1

                id : colour1
                Layout.preferredWidth:  200
                Layout.preferredHeight : 200
                Layout.fillWidth: true
                Layout.fillHeight: true

                color : "#ffc0cb"
                MouseArea {
                           anchors.fill: parent
                                    onClicked: {
                                        colorDialog.caller = colour1
                                        colorDialog.color = colour1.color
                                        colorDialog.open()
                                    }
                                }
        }
        Rectangle{
            Layout.row : 0
            Layout.column : 1
            Layout.columnSpan : 1

                    id : colour2
                    Layout.preferredWidth:  200
                    Layout.preferredHeight : 200
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    color : "#ffae32"
                MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                colorDialog.caller = colour2
                                colorDialog.color = colour2.color
                                colorDialog.open()
                            }
                          }

        }

        Rectangle{
                    id : mixed
                    Layout.row : 1
                    Layout.columnSpan : 2
                    Layout.preferredWidth:  400
                    Layout.preferredHeight : 200
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color : Qt.rgba(
                                colour1.color.r+ (mix.value *(colour2.color.r - colour1.color.r)),
                                colour1.color.g+ (mix.value *(colour2.color.g - colour1.color.g)),
                                colour1.color.b+ (mix.value *(colour2.color.b - colour1.color.b)),
                                1.0 )

        }
        Rectangle{
                    id : gradient
                    Layout.row : 2
                    Layout.columnSpan : 2
                    Layout.preferredWidth:  400
                    Layout.preferredHeight : 200
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    gradient: Gradient {
                            GradientStop { position: 0.0; color: colour1.color }
                            GradientStop { position: 1.0; color: colour2.color }

                    }
        }

        Slider {

            Layout.row : 3
            Layout.columnSpan: 2
            implicitWidth: colour1.width*2
            id : mix
            from : 0.0
            to : 1.0
            value : 0.5
        }

    } // end grid layout

    ColorDialog {
        id: colorDialog
        property var caller
        title: "Please choose a color"
        onAccepted: {
            caller.color = this.color
            this.close()
        }
        onRejected: {
            this.close()
        }
        Component.onCompleted: visible = false
    }

}

