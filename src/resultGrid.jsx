import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
// import { AgGridReact } from "@ag-grid-community/react";
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional Theme applied to the Data Grid
import { SetFilterModule } from "@ag-grid-enterprise/set-filter";
import { ModuleRegistry } from "@ag-grid-community/core";

import { useCallback, useEffect, useMemo, useState } from 'react';
import axios from 'axios';

ModuleRegistry.registerModules([
  // ClientSideRowModelModule,
  // ColumnsToolPanelModule,
  // FiltersToolPanelModule,
  // MenuModule,
  SetFilterModule,
]);

const ResultGrid = ({data, formData}) =>{

    const [rowData, setRowData] = useState([]);
    const [columnDefs, setColumnDefs] = useState([]);
    const defaultColDef = useMemo(() => {
        return {
          flex: 1,
          minWidth: 150,
          filter: true,
          // cellDataType: false,
          floatingFilter: true,
        //   suppressHeaderMenuButton: true,
        };
      }, []);

    // const onGridReady = useCallback((params) => {
    //     params.api.getToolPanelInstance("filters").expandFilters();
    //   }, []);
    
    // useEffect(() => {
    //     axios.get('http://127.0.0.1:5000/api/get-data')
    //       .then((response) => {
    //         const data = response.data;
            
    //         // Dynamically create columns based on the keys from the first row
            // if (data.length > 0) {
            //   const columns = Object.keys(data[0]).map(key => ({
            //     headerName: key.charAt(0).toUpperCase() + key.slice(1), // Capitalize column headers
            //     field: key,
            //     // filter: "agSetColumnFilter",
            //     floatingFilter: true,
            //   }));
            //   setColumnDefs(columns);
            // }
            // setRowData(data);
    //       })
    //       .catch((error) => {
    //         console.error("Error fetching data:", error);
    //       });
    //   }, []);

    const getRowStyle = (params) => {
      return {
        backgroundColor: params.data[2024] < formData.Rank ? 'red' : 'green',
        color: 'white',  // Optional: to make text readable
      };
    };

      useEffect(() =>{
        if (data.length > 0) {
          const columns = Object.keys(data[0]).map(key => ({
            headerName: key.charAt(0).toUpperCase() + key.slice(1), // Capitalize column headers
            field: key,
            // filter: "agSetColumnFilter",
            floatingFilter: true,
          }));
          setColumnDefs(columns);
        }
        setRowData(data);
      },[data]);

    return(
        <div
        className="ag-theme-alpine-dark" // applying the Data Grid theme
        style={{ height: 500 }} // the Data Grid will fill the size of the parent container
       >
         <AgGridReact
             rowData={rowData}
             columnDefs={columnDefs}
             defaultColDef={defaultColDef}
            //  sideBar={"filters"}
            //  onGridReady={onGridReady}
             getRowStyle={getRowStyle}
             pagination={true}
             paginationPageSize={20}
         />
       </div>
    );
}

export default ResultGrid;