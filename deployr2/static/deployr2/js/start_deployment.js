function loadBuilds(buildId, branch) {
    return $.get('/get_builds', {branch: branch, build_id: buildId});
}

var viewModel = {
    frontendBuilds: ko.observableArray(),
    backendBuilds: ko.observableArray()
};

$(function() {
    var $radioInputs = $('input[type="radio"]');
    var $selects = $('select');

    $radioInputs.change(function(ev) {
        $radioInputs.attr('disabled', 'disabled');
        $selects.attr('disabled', 'disabled');

        var buildType = ev.target.name === 'frontend_branch' ? 'Techdev_TrackrFrontend' : 'Techdev_TrackrBackend';

        function buildsLoaded(builds) {
            // replace build array
            if(ev.target.name === 'frontend_branch') {
                viewModel.frontendBuilds(builds);
            } else {
                viewModel.backendBuilds(builds);
            }

            $radioInputs.removeAttr('disabled');
            $selects.removeAttr('disabled');
        }

        loadBuilds(buildType, ev.target.value).done(buildsLoaded);
    });

    ko.applyBindings(viewModel);
});