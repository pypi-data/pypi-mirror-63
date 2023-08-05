$("#info").hide();

$.ajax({url: "/performance/cpu/brand_bits", success: function(brand_bits) {
    $.ajax({url: "/performance/cpu/cores", success: function(cores) {
        brand_bits = JSON.parse(brand_bits);
        cores = JSON.parse(cores);

        $("#brand").text(brand_bits['brand']);
        $("#cores").text(cores['physical'] + ' cores / ' + cores['logical'] + ' threads');
        $("#architecture").text(brand_bits['bits'] + '-bit architecture');

        $("#info").show();
        $("#load").remove();
    }});
}});