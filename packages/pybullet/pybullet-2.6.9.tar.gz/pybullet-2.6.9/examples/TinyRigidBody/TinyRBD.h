#ifndef TINY_RBD_H
#define TINY_RBD_H

#include "Fix64Matrix3x3.h"

enum TinyRBDEnumCollisionTypes
{
	TINYRBD_PLANE_TYPE,
	TINYRBD_SPHERE_TYPE,
	TINYRBD_BOX_TYPE
};

struct TinyRBDPlane
{
	Fix64Vector3   m_normal;
	Fix64Scalar    m_planeConstant;
};

struct TinyRBDSphere
{
	Fix64Scalar    m_radius;

	void computeLocalInertia(Fix64Scalar mass, Fix64Vector3& localInertia)
	{
		Fix64Scalar elem = Fix64Scalar::fromScalar(0.4) * mass * m_radius*m_radius;
		localInertia.setValue(elem, elem, elem);
	}
};

struct TinyRBDBox
{
	Fix64Vector3 m_halfExtents;
	void computeLocalInertia(Fix64Scalar mass, Fix64Vector3& localInertia)
	{
		Fix64Vector3 sqrSz = m_halfExtents * Fix64Scalar::two();
		sqrSz = mulPerElem(sqrSz, sqrSz);
		Fix64Scalar twelve = Fix64Scalar::fromScalar(12);
		localInertia.setValue((mass*(sqrSz.getY() + sqrSz.getZ())) / twelve, (mass*(sqrSz.getX() + sqrSz.getZ())) / twelve, (mass*(sqrSz.getX() + sqrSz.getY())) / twelve);
	}
};

struct TinyRBDCollisionShape
{
	TinyRBDEnumCollisionTypes m_type;
	union
	{
		TinyRBDPlane     m_plane;
		TinyRBDSphere    m_sphere;
		TinyRBDBox       m_box;
	};

};



struct TinyRBDPose
{

	Fix64Vector3		m_position;
	Fix64Quaternion	m_orientation;
	TinyRBDPose()
		:m_position(Fix64Vector3::makeIdentity()),
		m_orientation(Fix64Quaternion::makeIdentity())
	{
	}

	Fix64Vector3 transformPoint(const Fix64Vector3& pointIn)
	{
		Fix64Vector3 rotPoint = Fix64QuatRotate(m_orientation, pointIn);
		return rotPoint + m_position;
	}

	Fix64Vector3 inverseTransformPoint(const Fix64Vector3& pointIn) const
	{
		Fix64Vector3 pointOut = pointIn - m_position;
		Fix64Quaternion invOrientation = m_orientation.inverse();
		pointOut = Fix64QuatRotate(invOrientation, pointOut);
		return pointOut;
	}


};

struct TinyRBDContactPoint
{
	Fix64Vector3 m_localPointA;
	Fix64Vector3 m_localPointB;
	Fix64Vector3 m_normalOnB;
	Fix64Scalar  m_distance;
	int m_bodyA;
	int m_bodyB;
};

#endif//TINY_RBD_H
