<template>
    <div>
        <div v-if="trigger.type == 'interval'" @click="removeTrigger">
            <p>Every</p>
            <h2>{{ trigger.options.interval }}</h2>
            <p>seconds</p>
        </div>

        <div v-if="trigger.type == 'cron'" @click="removeTrigger">
            <p>CRON expression</p>
            <h3><code>{{ trigger.options.expression }}</code></h3>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Trigger',
    props: {
        trigger: {
            type: Object,
            required: true
        }
    },
    methods: {
        removeTrigger: function() {
            this.$emit('removeTrigger')
        }
    }
}
</script>

<style lang="scss" scoped>
div {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height: 200px;
    width: 200px;
    border: 1px solid lightgray;
    border-radius: 4px;
    transition: .1s background;

    &:hover {
        cursor: pointer;
        background: darken(#fff, 5%);
    }

    p {
        margin: 0;
    }

    h2 {
        margin: 0;
        margin-top: 0 !important;
        font-size: 3rem;
    }

    h3 {
        margin-top: 0 !important;
        font-size: 1.2rem;
    }
}


</style>