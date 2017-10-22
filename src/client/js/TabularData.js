TabularDataClass = React.createClass({
    render() {
        let data = this.props['data'];

        return React.DOM.table({'key':'table'}, [
            React.DOM.thead({'key':'thead'}, [
                React.DOM.tr({'key':'tr'}, Object.keys(data).map(key => React.DOM.th({'key':key}, key)))
            ]),
            React.DOM.tbody({'key':'tbody'}, )
        ]);
    }
});

TabularData = React.createFactory(TabularDataClass);