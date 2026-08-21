document.querySelectorAll('[data-sortable-table]').forEach(function (tableContainer) {
  var tableBody = tableContainer.querySelector('tbody');
  var sortButtons = tableContainer.querySelectorAll('[data-sort]');

  tableContainer.querySelectorAll('[data-sortable-table-row]').forEach(function (row) {
    var expandButton = row.querySelector('.sortable-table__expand');

    if (expandButton) {
      expandButton.addEventListener('click', function () {
        var detail = document.getElementById(this.getAttribute('aria-controls'));
        var expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', String(!expanded));
        this.setAttribute('title', expanded ? 'Show details' : 'Hide details');
        detail.hidden = expanded;
      });
    }
  });

  sortButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var header = this.closest('th');
      var direction = header.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
      var sortKey = this.getAttribute('data-sort');
      var rows = Array.from(tableBody.querySelectorAll('[data-sortable-table-row]'));

      rows.sort(function (firstRow, secondRow) {
        var firstValue = firstRow.dataset[sortKey].toLowerCase();
        var secondValue = secondRow.dataset[sortKey].toLowerCase();
        return direction === 'ascending'
          ? firstValue.localeCompare(secondValue)
          : secondValue.localeCompare(firstValue);
      });

      sortButtons.forEach(function (sortButton) {
        sortButton.closest('th').setAttribute('aria-sort', 'none');
      });
      header.setAttribute('aria-sort', direction);
      rows.forEach(function (row) {
        tableBody.appendChild(row);
        var expandButton = row.querySelector('.sortable-table__expand');
        if (expandButton) {
          tableBody.appendChild(document.getElementById(expandButton.getAttribute('aria-controls')));
        }
      });
    });
  });
});
