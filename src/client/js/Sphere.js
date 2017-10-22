SphereClass = React.createClass({
    render() {
        return React.createElement(
            ReactTHREE.Sphere,
            {
                radius: 10,
                horizontalSegments: 10,
                verticalSegments: 10
            }
        );
    }
});

Sphere = React.createFactory(SphereClass);