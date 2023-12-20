<!-- CrimeTable.vue -->
<script>
export default {
  props: {
    crimes: Array,
    neighborhoods: Object,
    styleTableRows: Function,
    fixBlock: Function,
    dataMarker: Function,
    deleteCase: Function,
  },
};
const violentCodes = [2619, 810, 861, 862, 863, 100, 110, 120, 210, 220, 400, 410, 411, 412, 420, 421, 422,
                      430, 431, 432, 440, 441, 442, 450, 451, 452, 453, 300, 311, 312, 314, 321, 322, 323, 
                      324, 331, 333, 334, 341, 342, 343, 344, 351, 352, 353, 354, 361, 363, 364, 371, 373, 374];
const propCodes = [1400, 1401, 1410, 1415, 1416, 1420, 1425, 1426, 1430, 1435, 1436, 900, 901, 903, 905, 911, 913,
                   915, 921, 922, 923, 925, 931, 933, 941, 942, 951, 961, 971, 972, 975, 981, 982, 700, 710, 711, 712, 720,
                   721, 722, 730, 731, 732, 600, 603, 611, 612, 613, 614, 621, 622, 623, 630, 631, 632, 633, 640, 641, 642, 643,
                   651, 652, 653, 661, 662, 663, 671, 672, 673, 681, 682, 683, 691, 692, 693, 500, 510, 511, 513, 515, 516,
                   520, 521, 523, 525, 526, 530, 531, 533, 535, 536, 540, 541, 546, 553, 543, 545, 550, 551, 555, 556, 560, 
                   561, 563, 565, 566];
const otherCodes = [9986, 9959, 9954, 3100, 1800, 1810, 1811, 1813, 1814, 1815, 1820, 1822, 1823, 1824, 1825, 1830,
                    1835, 1840, 1841, 1842, 1843, 1844, 1845, 1850, 1855, 1860, 1865, 1870, 1880, 1885];



function getRowColorClass(code) {
    // Define your logic for assigning colors based on code values
    if (violentCodes.includes(code)) {
        return 'row-color-a';
    } else if (propCodes.includes(code)) {
        return 'row-color-b';
    } else if (otherCodes.includes(code)) {
        return 'row-color-c';
    } else {
        return ''; // Default color or no additional class
    }
}


const styleTableRows = (incident) => {
  const lowerCaseIncident = incident.toLowerCase();

  if (
    lowerCaseIncident.includes("arson") ||
    lowerCaseIncident.includes("assault") ||
    lowerCaseIncident.includes("homicide") ||
    lowerCaseIncident.includes("murder") ||
    lowerCaseIncident.includes("rape") ||
    lowerCaseIncident.includes("robbery")
  ) {
    return "highlight-red"; // Violent crimes - RED
  } else if (
    lowerCaseIncident.includes("burglary") ||
    lowerCaseIncident.includes("graffiti") ||
    lowerCaseIncident.includes("property") ||
    lowerCaseIncident.includes("theft")
  ) {
    return "highlight-orange"; // Property damage crimes - ORANGE
  } else {
    return "violent-crime-odd"; // Any other crime not mentioned above - YELLOW
  }
};

</script>
<template>
  <div>
    <table style="overflow-y: scroll">
      <thead style="position: sticky">
        <tr>
          <th>Date</th>
          <th>Incident type</th>
          <th>Police grid</th>
          <th>Neighborhood</th>
          <th>Block</th>
          <th></th>
          <th></th>
        </tr>
      </thead>

      <tbody id="tablebody" style="text-align: center; font-size: small">
        <tr
          v-for="crime in crimes"
          :key="crime.case_number"
          class="styleTableRows(crime.incident)"
        >
          <td>{{ crime.date }}</td>
          <td>{{ crime.incident }}</td>
          <td>{{ crime.police_grid }}</td>
          <td>{{ neighborhoods[crime.neighborhood_number] }}</td>
          <td>{{ fixBlock(crime.block) }}</td>
          <td>
            <button @click="dataMarker(crime)">View</button>
          </td>
          <td>
            <button @click="deleteCase(crime.case_number)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
    <br />
  </div>
</template>


<style scoped>
#tablebody td {
  height: 20px;
}

.custom-style {
  background-color: lightblue;
  font-size: 16px;
  /* Add more styles as needed */
}
.violent-crime-even,
.violent-crime-odd {
  background-color: red;
}

.property-crime-even,
.property-crime-odd {
  background-color: blue;
}

.other-crime-even,
.other-crime-odd {
  background-color: orange;
}
</style>
