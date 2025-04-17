import { useTheme } from '@emotion/react';
import { Container, CssBaseline, AppBar, Toolbar, Typography, Box, MenuItem, FormControl, InputLabel, ThemeProvider, createTheme, Button, Select, Stack, TextField, Chip, OutlinedInput, Checkbox, ListItemText, CircularProgress, Backdrop } from '@mui/material';
import React, { useState } from 'react';
import { defaultFormData, universityList, branchList, districtList } from './Constants';
import axios from 'axios';
const StudentForm = ({updateData}) => {
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    const handleClose = () => {
      setOpen(false);
    };
    const handleOpen = () => {
      setOpen(true);
    };
    const [formData, setFormData] = useState(defaultFormData);
    const [branchData, setBranchData] = useState(branchList.sort());
    const ITEM_HEIGHT = 48;
    const ITEM_PADDING_TOP = 8;
    const MenuProps = {
      PaperProps: {
        style: {
          maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
          width: 250,
        },
      },
    };

    function getStyles(name, personName, theme) {
      return {
        fontWeight:
          personName.indexOf(name) === -1
            ? theme.typography.fontWeightRegular
            : theme.typography.fontWeightMedium,
      };
    }
    
    const handleChange = (event) => {
      const { name, value } = event.target;
      setFormData({
        ...formData,
        [name]: value,
      });
      if (name === 'PrefferedDistrict'){
        axios.post('http://127.0.0.1:5000/api/getCollegeList', {
            'districtList': value
        })
        .then((response) => {
          const data = response.data;
          if (data.length > 0) {
            setBranchData(data);
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
    };

    const handleSubmit = async (e) => {
      handleOpen()
      e.preventDefault();
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/formSubmit', formData);
        console.log('Response from backend:', response.data);
        handleClose();
        updateData(response.data, formData);
      } catch (error) {
        handleClose();
        console.error('There was an error submitting the form:', error);
      }     
    };

    const handleReset = () => {
      setFormData(defaultFormData);
    };
    
    return (
        <>
        <Backdrop
          sx={(theme) => ({ color: '#fff', zIndex: theme.zIndex.drawer + 1 })}
          open={open}
          onClick={handleClose}
        >
          <CircularProgress color="inherit" />
        </Backdrop>
        <form>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} style={{margin:'10px 0', justifyContent:'center', display:'flex', alignItems:'center'}}>
        <TextField id="outlined-basic" label="Rank" type="number" name="Rank" value={formData.Rank} onChange={handleChange} variant="outlined" size='small' sx={{width:'150px'}} required/>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="Gender-select-label">Gender</InputLabel>
          <Select
            labelId="Gender-select-label"
            id="Gender"
            value={formData.Gender}
            onChange={handleChange}
            autoWidth
            label="Gender"
            name="Gender"
          >
            <MenuItem value='Male'>Male</MenuItem>
            <MenuItem value='Female'>Female</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="Caste-select-label">Caste</InputLabel>
          <Select
            labelId="Caste-select-label"
            id="Caste"
            value={formData.Caste}
            onChange={handleChange}
            autoWidth
            label="Caste"
            name="Caste"
          >
            <MenuItem value='OPEN'>OPEN</MenuItem>
            <MenuItem value='OBC'>OBC</MenuItem>
            <MenuItem value='SEBC'>SEBC</MenuItem>
            <MenuItem value='SC'>SC</MenuItem>
            <MenuItem value='ST'>ST</MenuItem>
            <MenuItem value='VJ'>VJ</MenuItem>
            <MenuItem value='NT'>NT</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="EWS-select-label">EWS</InputLabel>
          <Select
            labelId="EWS-select-label"
            id="EWS"
            value={formData.EWS}
            onChange={handleChange}
            autoWidth
            label="EWS"
            name="EWS"
          >
            <MenuItem value='Yes'>Yes</MenuItem>
            <MenuItem value='No'>No</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="PWD-select-label">PWD</InputLabel>
          <Select
            labelId="PWD-select-label"
            id="PWD"
            value={formData.PWD}
            onChange={handleChange}
            autoWidth
            label="PWD"
            name="PWD"
          >
            <MenuItem value='Yes'>Yes</MenuItem>
            <MenuItem value='No'>No</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="DEF-select-label">DEF</InputLabel>
          <Select
            labelId="DEF-select-label"
            id="DEF"
            value={formData.DEF}
            onChange={handleChange}
            autoWidth
            label="DEF"
            name="DEF"
          >
            <MenuItem value='Yes'>Yes</MenuItem>
            <MenuItem value='No'>No</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="TFWS-select-label">TFWS</InputLabel>
          <Select
            labelId="TFWS-select-label"
            id="TFWS"
            value={formData.TFWS}
            onChange={handleChange}
            autoWidth
            label="TFWS"
            name="TFWS"
          >
            <MenuItem value='Yes'>Yes</MenuItem>
            <MenuItem value='No'>No</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="ORPHAN-select-label">ORPHAN</InputLabel>
          <Select
            labelId="ORPHAN-select-label"
            id="ORPHAN"
            value={formData.ORPHAN}
            onChange={handleChange}
            autoWidth
            label="ORPHAN"
            name="ORPHAN"
          >
            <MenuItem value='Yes'>Yes</MenuItem>
            <MenuItem value='No'>No</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 100 }} size='small' required>
          <InputLabel id="MI-select-label">MI</InputLabel>
          <Select
            labelId="MI-select-label"
            id="MI"
            value={formData.MI}
            onChange={handleChange}
            autoWidth
            label="MI"
            name="MI"
          >
            <MenuItem value='Yes'>Yes</MenuItem>
            <MenuItem value='No'>No</MenuItem>
          </Select>
        </FormControl>
      </Stack>
      <Stack direction={{ xs: 'column', sm: 'column' }} spacing={1} style={{margin:'10px 0', justifyContent:'center', alignItems:'center'}}>
        <FormControl sx={{ m: 1, minWidth: 200}} size='small' required>
          <InputLabel id="Home-University-select-label">Your University</InputLabel>
          <Select
            labelId="Home-University-select-label"
            id="Home-University"
            value={formData.HomeUniversity}
            onChange={handleChange}
            autoWidth
            label="Home University"
            name="HomeUniversity"
            required
            style={{width:'500px'}}
          >
            {universityList.map((name) => (
              <MenuItem
                key={name}
                value={name}
              >
                {name}
              </MenuItem>
            ))}
          </Select>
          </FormControl>
          <FormControl sx={{ m: 1, minWidth: 500 }} size='small'>
            <InputLabel id="Preffered-District-label">Preffered District</InputLabel>
            <Select
              labelId="Preffered-District-label"
              id="Preffered-District"
              multiple
              value={formData.PrefferedDistrict}
              onChange={handleChange}
              name="PrefferedDistrict"
              input={<OutlinedInput id="select-multiple-district" label="Preffered District" />}
              renderValue={(selected) => selected.join(', ')}
              MenuProps={MenuProps}
            >
              {districtList.map((name) => (
                <MenuItem key={name} value={name}>
                  <Checkbox checked={formData.PrefferedDistrict.indexOf(name) > -1} />
                  <ListItemText primary={name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {/* <FormControl sx={{ m: 1, minWidth: 300 }} size='small'>
            <InputLabel id="Preffered-College-label">Preffered Colleges</InputLabel>
            <Select
              labelId="Preffered-College-label"
              id="Preffered-College"
              multiple
              value={formData.PrefferedBranch}
              name="PrefferedCollege"
              onChange={handleChange}
              input={<OutlinedInput id="select-multiple-College" label="Preffered College" />}
              renderValue={(selected) => selected.join(', ')}
              MenuProps={MenuProps}
            >
              {branchList.map((name) => (
                <MenuItem key={name} value={name}>
                  <Checkbox checked={formData.PrefferedBranch.indexOf(name) > -1} />
                  <ListItemText primary={name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl> */}
          <FormControl sx={{ m: 1, minWidth: 500 }} size='small'>
            <InputLabel id="Preffered-Branch-label">Preffered Branch</InputLabel>
            <Select
              labelId="Preffered-Branch-label"
              id="Preffered-Branch"
              multiple
              value={formData.PrefferedBranch}
              name="PrefferedBranch"
              onChange={handleChange}
              input={<OutlinedInput id="select-multiple-branch" label="Preffered Branch" />}
              renderValue={(selected) => selected.join(', ')}
              MenuProps={MenuProps}
            >
              {branchData.map((name) => (
                <MenuItem key={name} value={name}>
                  <Checkbox checked={formData.PrefferedBranch.indexOf(name) > -1} />
                  <ListItemText primary={name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Stack>
        <Stack direction='row' spacing={1} style={{margin:'10px 0', justifyContent:'center'}}>
          <Button variant='outlined' type='submit' color="primary" size='small' style={{height : '40px'}} onClick={handleSubmit} >Submit</Button>
          <Button variant='outlined' color="primary" size='small' style={{height : '40px'}} onClick={handleReset}>Reset</Button>
        </Stack>
        </form>
        </>
      )
}

export default StudentForm;