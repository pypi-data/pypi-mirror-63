(function($){
    $(document).ready(function(){
        $.fn.django_cascading_dropdown_widget = function(){
            $(this).change(function(){
                var value = $(this).val();
                var name = $(this).attr("data-name");
                var show_name = name + "-" + value;
                var input = $(this).prevAll(".django-cascading-dropdown-widget-hidden-input");
                $(this).nextAll().hide();
                var next_select = $(this).nextAll(".django-cascading-dropdown-widget-select[data-name=" + show_name + "]");
                if(next_select.length > 0){
                    next_select.show();
                    input.val("");
                }else{
                    input.val(value);
                }
            });
        };
        $(".django-cascading-dropdown-widget-select").django_cascading_dropdown_widget();
        $(document.body).arrive(".django-cascading-dropdown-widget-select", function(){
            $(this).django_cascading_dropdown_widget();
        });
    });
})(jQuery);
