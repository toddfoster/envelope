/* start: http://blogs.html5andcss3.org/show-and-hide-div-with-javascript/ */
function showhide()
{
  var fromHidden  = document.getElementById("fromHidden");
  var fromShowing = document.getElementById("fromShowing");
  var fromEntry   = document.getElementById("fromEntry");

  if (fromHidden.style.display !== "none") {
    fromHidden.style.display = "none";
    fromShowing.style.display = "block";
    fromEntry.style.display = "block";
  }
  else {
    fromHidden.style.display  = "block";
    fromShowing.style.display = "none";
    fromEntry.style.display   = "none";
  }
}
