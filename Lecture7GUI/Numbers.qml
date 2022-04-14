import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.0

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Numbers")
    GridLayout
    {
       anchors.fill: parent
       rows:   6
       columns:   2
        SpinBox {
            Layout.row : 0
            Layout.column: 0
            id: spinBox
        }
        SpinBox {

            Layout.row : 0
            Layout.column: 1

            id: spinbox2
            from: 0
            value: 110
            to: 100 * 100
            stepSize: 100
            property int decimals: 2
            property real realValue: value / 100

            validator: DoubleValidator {
                bottom: Math.min(spinbox2.from, spinbox2.to)
                top:  Math.max(spinbox2.from, spinbox2.to)
            }

            textFromValue: function(value, locale) {
                return Number(value / 100).toLocaleString(locale, 'f', spinbox2.decimals)
            }

            valueFromText: function(text, locale) {
                return Number.fromLocaleString(locale, text) * 100
            }
        }

        Dial {
            id: dial
            Layout.row: 2
            Layout.column: 0

        }
        Dial {
            id: dial2
            Layout.row: 2
            Layout.column: 1

        }



    RangeSlider {
        id: rangeSlider
        x: 69
        y: 438
        first.value: 0.25
        second.value: 0.75
    }

    Slider {
        id: slider
        x: 368
        y: 423
        value: 0.5
    }

  }

}
