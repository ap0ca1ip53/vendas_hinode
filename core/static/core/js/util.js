/**
 * Created by ap0ca1ip53 on 31/10/16.
 */
$(document).ready(function ()
{
    $(".exclui").click(function ()
    {
        $(".window-popup").show(300);
    });

    $("#buton-popup-close").click(function () {
        $(".window-popup").hide(300);
    });
});