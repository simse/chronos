<template>
    <div class="navbar">
        <div class="logo">
            <h1>Chronos</h1>
        </div>

        <div class="items">
            <ul>
                <li><a href="#">Scripts</a></li>
                <li><a href="#">Logs</a></li>
                <li><a href="#">Settings</a></li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Navbar'
}
</script>

<style lang="scss" scoped>
.navbar {
    display: flex;
    color: #000;
    background: #fff;
    border-bottom: 1px solid lightgrey;
    padding: 16px 24px;
    align-items: center;
}

.logo h1 {
    font-size: 1.4rem;
    font-weight: 700;
}

.items {
    padding: 0 20px;
    ul {
        display: flex;

        a {
            padding: 0 12px;
            display: block;
        }
    }
}
</style>