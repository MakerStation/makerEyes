View3DClass = React.createClass({

    render() {
        var MainCameraElement = React.createElement(
        ReactTHREE.PerspectiveCamera,
        {
            name:'maincamera',
            fov:'75',
            aspect:this.props.width/this.props.height,
            near:1,
            far:5000,
            position: new THREE.Vector3(0,0,600),
            lookat: new THREE.Vector3(0,0,0)
        }
        );

        return React.createElement(
            ReactTHREE.Renderer,
            {width:this.props.width, height:this.props.height},
            React.createElement(
                ReactTHREE.Scene,
                {width:this.props.width, height:this.props.height, camera:'maincamera'},
                MainCameraElement,
                null    //React.createElement(Sphere, this.props)
            )
        );
    }
/*
    render() {
        return React.createElement('h1', null, '3D View');
    }
*/
});

View3D = React.createFactory(View3DClass);