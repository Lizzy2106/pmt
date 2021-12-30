// Call the dataTables jQuery plugin
	alert('table');
$(document).ready(function() {
	var table = $('#dataTable').DataTable(
		responsive: true
	);
	//Exportable table
	$('#dataTable').DataTable({
		dom: 'Bfrtip',
		responsive: true,
		buttons: [
			'copy', 'csv', 'excel', 'pdf', 'print'
		]
	});
	$('#dataTable').DataTable( {
		"pagingType": "full_numbers"
	} );

	$('#myInput').on( 'keyup', function () {
		table.search( this.value ).draw();
	} );
});
