import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { PackageSearch, Plus, ArrowRight } from 'lucide-react'
import { apiClient, Product } from '../api/client'
import './Dashboard.css'

export default function Dashboard() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [newProductName, setNewProductName] = useState('')

  const fetchProducts = async () => {
    try {
      const { data } = await apiClient.get<Product[]>('/products/')
      setProducts(data)
    } catch (error) {
      console.error("Failed to fetch products", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newProductName.trim()) return
    try {
      await apiClient.post('/products/', { name: newProductName, description: "New product concept" })
      setNewProductName('')
      fetchProducts()
    } catch (error) {
      console.error("Failed to create product", error)
    }
  }

  return (
    <div className="dashboard-container animate-fade-in">
      <header className="dashboard-header">
        <div>
          <h2 className="dashboard-title">Active Products</h2>
          <p className="dashboard-subtitle">Manage your product lifecycle portfolio</p>
        </div>
        <form onSubmit={handleCreateProduct} className="create-form">
          <input
            type="text"
            placeholder="New Product Name"
            className="input-field"
            value={newProductName}
            onChange={e => setNewProductName(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">
            <Plus size={20} /> Create
          </button>
        </form>
      </header>

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
        </div>
      ) : products.length === 0 ? (
        <div className="empty-state glass-panel">
          <PackageSearch className="empty-icon" />
          <h3>No products found</h3>
          <p>Create your first product to start the lifecycle.</p>
        </div>
      ) : (
        <div className="product-grid">
          {products.map(product => (
            <Link 
              key={product.id} 
              to={`/product/${product.id}`}
              className="product-card glass-panel group"
            >
              <div className="card-glow"></div>
              <div className="card-header">
                <h3 className="card-title">{product.name}</h3>
                <span className={`badge badge-${product.status}`}>
                  {product.status}
                </span>
              </div>
              <p className="card-description">{product.description}</p>
              
              <div className="card-footer">
                <div className="phase-indicator">
                  <span className="phase-label">Phase</span>
                  <span className="phase-value">{product.current_phase.replace('_', ' ')}</span>
                </div>
                <div className="arrow-btn">
                  <ArrowRight size={20} />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
