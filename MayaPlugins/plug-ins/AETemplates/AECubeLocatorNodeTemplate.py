from maya.app.general.AETemplate import Template


class AECubeLocatorNodeTemplate(Template):
    def setup(self):
        self.beginScrollLayout()

        # Custom section
        self.beginLayout("Cube Locator", collapse=False)
        self.addControl("width")
        self.addControl("height")
        self.addControl("depth")
        self.addControl("colour")
        self.addControl("textColour")
        self.endLayout()

        # Suppress volume from Extra Attributes since it is output-only
        self.suppress("volume")

        # Let Maya add any remaining attributes
        self.addExtraControls()

        self.endScrollLayout()
