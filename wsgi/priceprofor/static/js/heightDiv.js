$( document ).ready(function() {
    var heightsServices = $(".heightsServices").map(function() {
        return $(this).height();
    }).get(),

    maxHeight = Math.max.apply(null, heightsServices);

    $(".heightsServices").height(maxHeight);

    var heightsFeatureBisUp = $(".heightsFeatureBisUp").map(function() {
        return $(this).height();
    }).get(),

    maxHeight = Math.max.apply(null, heightsFeatureBisUp);

    $(".heightsFeatureBisUp").height(maxHeight);

    var heightsFeatureBis = $(".heightsFeatureBis").map(function() {
        return $(this).height();
    }).get(),

    maxHeight = 210;

    $(".heightsFeatureBis").height(maxHeight);
});