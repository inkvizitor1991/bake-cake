let CakeComponentsData = JSON.parse(document.getElementById('cake-components-data').textContent);

Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: {
                Levels: ['не выбрано'].concat(CakeComponentsData['levels']['quantity']),
                Forms: ['не выбрано'].concat(CakeComponentsData['forms']['figures']),
                Toppings: ['не выбрано', 'Без'].concat(CakeComponentsData['toppings']['names']),
                Berries: ['нет'].concat(CakeComponentsData['berries']['names']),
                Decors: [ 'нет'].concat(CakeComponentsData['decors']['names']),
            },
            Costs: {
                Levels: [0].concat(CakeComponentsData['levels']['prices']),
                Forms: [0].concat(CakeComponentsData['forms']['prices']),
                Toppings: [0, 0].concat(CakeComponentsData['toppings']['prices']),
                Berries: [0].concat(CakeComponentsData['berries']['prices']),
                Decors: [0].concat(CakeComponentsData['decors']['prices']),
                Words: 500
            },
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,

            Name: '',
            Phone: null,
            Email: null,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: ''
        }
    },
    methods: {
        ToStep4() {
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        },
        SubmitOrder() {
            //Тут выведен в консоль объект, описывающий заказ полностью. Сработает только после прохождения валидации 2ой формы:
            console.log(JSON.stringify({
                Cost: this.Cost,
                Levels: this.DATA.Levels[this.Levels],
                Form: this.DATA.Forms[this.Form],
                Topping: this.DATA.Toppings[this.Topping],
                Berries: this.DATA.Berries[this.Berries],
                Decor: this.DATA.Decors[this.Decor],
                Words: this.Words,
                Comments: this.Comments,
                Name: this.Name,
                Phone: this.Phone,
                Email: this.Email,
                Address: this.Address,
                Dates: this.Dates,
                Time: this.Time,
                DelivComments: this.DelivComments,
            }, null ,2))
        }
    },
    computed: {
        Cost() {
            let W = this.Words ? this.Costs.Words : 0
            return this.Costs.Levels[this.Levels] + this.Costs.Forms[this.Form] +
                this.Costs.Toppings[this.Topping] + this.Costs.Berries[this.Berries] +
                this.Costs.Decors[this.Decor] + W
        }
    }
}).mount('#VueApp')
