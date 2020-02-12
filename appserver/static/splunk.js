// <![CDATA[
// <![CDATA[
//
// LIBRARY REQUIREMENTS
//
// In the require function, we include the necessary libraries and modules for
// the HTML dashboard. Then, we pass variable names for these libraries and
// modules as function parameters, in order.
//
// When you add libraries or modules, remember to retain this mapping order
// between the library or module and its function parameter. You can do this by
// adding to the end of these lists, as shown in the commented examples below.

require([
    "splunkjs/mvc",
    "splunkjs/mvc/utils",
    "splunkjs/mvc/tokenutils",
    "underscore",
    "jquery",
    "splunkjs/mvc/simplexml",
    "splunkjs/mvc/layoutview",
    "splunkjs/mvc/simplexml/dashboardview",
    "splunkjs/mvc/simplexml/dashboard/panelref",
    "splunkjs/mvc/simplexml/element/chart",
    "splunkjs/mvc/simplexml/element/event",
    "splunkjs/mvc/simplexml/element/html",
    "splunkjs/mvc/simplexml/element/list",
    "splunkjs/mvc/simplexml/element/map",
    "splunkjs/mvc/simplexml/element/single",
    "splunkjs/mvc/simplexml/element/table",
    "splunkjs/mvc/simplexml/element/visualization",
    "splunkjs/mvc/simpleform/formutils",
    "splunkjs/mvc/simplexml/eventhandler",
    "splunkjs/mvc/simplexml/searcheventhandler",
    "splunkjs/mvc/simpleform/input/dropdown",
    "splunkjs/mvc/simpleform/input/radiogroup",
    "splunkjs/mvc/simpleform/input/linklist",
    "splunkjs/mvc/simpleform/input/multiselect",
    "splunkjs/mvc/simpleform/input/checkboxgroup",
    "splunkjs/mvc/simpleform/input/text",
    "splunkjs/mvc/simpleform/input/timerange",
    "splunkjs/mvc/simpleform/input/submit",
    "splunkjs/mvc/searchmanager",
    "splunkjs/mvc/savedsearchmanager",
    "splunkjs/mvc/postprocessmanager",
    "splunkjs/mvc/simplexml/urltokenmodel"
    // Add comma-separated libraries and modules manually here, for example:
    // ..."splunkjs/mvc/simplexml/urltokenmodel",
    // "splunkjs/mvc/tokenforwarder"
    ],
    function(
        mvc,
        utils,
        TokenUtils,
        _,
        $,
        DashboardController,
        LayoutView,
        Dashboard,
        PanelRef,
        ChartElement,
        EventElement,
        HtmlElement,
        ListElement,
        MapElement,
        SingleElement,
        TableElement,
        VisualizationElement,
        FormUtils,
        EventHandler,
        SearchEventHandler,
        DropdownInput,
        RadioGroupInput,
        LinkListInput,
        MultiSelectInput,
        CheckboxGroupInput,
        TextInput,
        TimeRangeInput,
        SubmitButton,
        SearchManager,
        SavedSearchManager,
        PostProcessManager,
        UrlTokenModel

        // Add comma-separated parameter names here, for example:
        // ...UrlTokenModel,
        // TokenForwarder
        ) {

        var pageLoading = true;


        //
        // TOKENS
        //

        // Create token namespaces
        var urlTokenModel = new UrlTokenModel();
        mvc.Components.registerInstance('url', urlTokenModel);
        var defaultTokenModel = mvc.Components.getInstance('default', {create: true});
        var submittedTokenModel = mvc.Components.getInstance('submitted', {create: true});

        urlTokenModel.on('url:navigate', function() {
            defaultTokenModel.set(urlTokenModel.toJSON());
            if (!_.isEmpty(urlTokenModel.toJSON()) && !_.all(urlTokenModel.toJSON(), _.isUndefined)) {
                submitTokens();
            } else {
                submittedTokenModel.clear();
            }
        });

        // Initialize tokens
        defaultTokenModel.set(urlTokenModel.toJSON());

        function submitTokens() {
            // Copy the contents of the defaultTokenModel to the submittedTokenModel and urlTokenModel
            FormUtils.submitForm({ replaceState: pageLoading });
        }

        function setToken(name, value) {
            defaultTokenModel.set(name, value);
            submittedTokenModel.set(name, value);
        }

        function unsetToken(name) {
            defaultTokenModel.unset(name);
            submittedTokenModel.unset(name);
        }



        //
        // SEARCH MANAGERS
        //



        //
        // SPLUNK LAYOUT
        //

        $('header').remove();
        new LayoutView({"hideChrome": false, "hideSplunkBar": false, "hideAppBar": false})
            .render()
            .getContainerElement()
            .appendChild($('.dashboard-body')[0]);

        //
        // DASHBOARD EDITOR
        //

        new Dashboard({
            id: 'dashboard',
            el: $('.dashboard-body'),
            showTitle: true,
            editable: true
        }, {tokens: true}).render();


        //
        // VIEWS: VISUALIZATION ELEMENTS
        //
//
        // VIEWS: FORM INPUTS
        //
        let time_defaults = ['rt', 'rt-5m'];

        let input1 = new TimeRangeInput({
            id: 'input1',
            searchWhenChanged: true,
            default: {'latest_time': time_defaults[0], 'earliest_time': time_defaults[1]},
            earliest_time: '$form.time.earliest$',
            latest_time: '$form.time.latest$',
            el: document.querySelector('#input1')
        }, {tokens: true}).render();

        input1.on('change', function(newvalue) {
            FormUtils.handleValueChange(input1);
        });

        DashboardController.onReady(function() {
            if (!submittedTokenModel.has('earliest') && !submittedTokenModel.has('latest')) {
                submittedTokenModel.set({ earliest: '0', latest: '' });
            }
        });
        // Initialize time tokens to default
        if (!defaultTokenModel.has('earliest') && !defaultTokenModel.has('latest')) {
            defaultTokenModel.set({ earliest: '0', latest: '' });
        }

        submitTokens();

        //
        // DASHBOARD READY
        //

        DashboardController.ready();
        pageLoading = false;

    }
);
// ]]>
require(["splunkjs/mvc/searchmanager"], function(SearchManager) {
    const search_string = `
    index = test01
    | eval Time = _time
    | sort _time
    | table metric_value Time`;

    const search = new SearchManager({
        id: 'search1', 
        earliest_time: '$time.earliest$', 
        autostart: true, 
        status_buckets: 0, 
        sample_ratio: 1, 
        latest_time: '$time.latest$',
        search: search_string, 
        preview: true, 
        tokenDependencies: {}, 
        runWhenTimeIsUndefined: false
    }, {tokens: true, tokenNamespace: 'submitted'}); 

    const search_data = search.data('preview',{count:0}); 
    search_data.on('data', function() {

        if (search_data.data().rows.length === 0) return;
        if(this.last_data === JSON.stringify(search_data.data())) return;
        this.last_data = JSON.stringify(search_data.data());

        const data = transpose(search_data.data().rows);
        const metric_values = data[search_data.data().fields.indexOf('metric_value')];
        const times = data[search_data.data().fields.indexOf('Time')];

        // console.log(metric_values)
        // console.log(times)
        if (!window.addinng_points) addPoints();

        window.addinng_points = true;

        for(let i = 0; i < metric_values.length; i++) {
            addDataPoint(Number(times[i]), Number(metric_values[i]));
        }

    });
})


function transpose(matrix) {
	return matrix[0].map((col, i) => matrix.map(row => row[i]))
}