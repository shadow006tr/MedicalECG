function deleteGraph(graph_number)
{

    var container = document.getElementById('graph-container');
    var graph_to_delete = document.getElementById('graph_number_' + graph_number);

    graph_to_delete.remove();

    var navlead_to_delete = document.getElementById("navLead_" + graph_number).parentElement;
    navlead_to_delete.remove();


}