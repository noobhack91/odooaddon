/** @odoo-module **/

import { useState, useRef, onMounted } from '@odoo/owl';
import { rpc } from 'web.rpc';
import { DatePicker, Select } from 'web.OwlComponents'; // Assumes you have created or imported these OWL-compatible components.

class ContractManagement extends Component {
    setup() {
        this.customers = useState([]);
        this.items = useState([]);
        this.currency = useState(null);
        this.contractFiles = useState([]);
        this.startDate = useState(null);
        this.endDate = useState(null);
        this.remarks = useState('');
        this.error = useState(null);
        this.selectedVendor = useState(null);
        this.vendors = useState([]);
        this.itemOptions = useState([
            { value: 'item1', label: 'Item 1' },
            { value: 'item2', label: 'Item 2' },
        ]);
        this.selectedItems = useState([]);

        this.customerOptions = [
            { value: 'customer1', label: 'Customer 1' },
            { value: 'customer2', label: 'Customer 2' },
        ];

        this.currencyOptions = [
            { value: 'USD', label: 'USD' },
            { value: 'INR', label: 'INR' },
        ];

        onMounted(this.fetchVendors);
        onMounted(this.fetchItems);
    }

    async fetchVendors() {
        try {
            const response = await rpc('/api/vendors/?is_company=True', {});
            this.vendors = response.vendors.map(vendor => ({
                value: vendor.id,
                label: vendor.name,
            }));
        } catch (error) {
            this.error = 'Error fetching vendors';
            console.error(error);
        }
    }

    async fetchItems() {
        try {
            const response = await rpc('/api/products', {});
            const fetchedItems = response.products.map(item => ({
                value: item.id,
                label: item.name,
            }));
            this.itemOptions = [...this.itemOptions, ...fetchedItems];
        } catch (error) {
            this.error = 'Error fetching items';
            console.error(error);
        }
    }

    handleFileChange(customerIndex, file) {
        this.contractFiles[customerIndex] = file;
    }

    handleRemarksChange(event) {
        this.remarks = event.target.value;
    }

    handleSubmit() {
        console.log('Submitting:', {
            selectedVendor: this.selectedVendor,
            customers: this.customers,
            items: this.items,
            contractFiles: this.contractFiles,
            startDate: this.startDate,
            endDate: this.endDate,
            remarks: this.remarks,
        });
    }

    handleItemSelect(selectedItems) {
        this.items = selectedItems.map(item => ({
            id: item.value,
            name: item.label,
            defaultRate: '',
            customerRates: Array(this.customers.length).fill(''),
        }));
    }

    handleRateChange(index, customerIndex, value) {
        this.items[index].customerRates[customerIndex] = value;
    }
}
ContractManagement.template = 'lims_inventory.ContractManagementTemplate';
export default ContractManagement;
